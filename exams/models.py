from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import json
import uuid


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.course_name


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    time_limit = models.IntegerField(help_text='Time limit in minutes')
    total_points = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    passing_score = models.IntegerField(default=60, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_attempts = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exams'
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
    
    def __str__(self):
        return f"{self.exam_title} ({self.course.course_name})"
    
    def get_total_questions(self):
        return self.questions.count()
    
    def is_available(self):
        """Check if exam is currently available for taking"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.start_time and now < self.start_time:
            return False
        if self.end_time and now > self.end_time:
            return False
        return True


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    question_id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=10)  # 'A', 'B', 'C', 'D', 'True', 'False'
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, validators=[MinValueValidator(0.1)])
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['sort_order', 'question_id']
    
    def __str__(self):
        return f"Q{self.sort_order}: {self.question_text[:50]}..."
    
    def get_options(self):
        if self.question_type == 'multiple_choice':
            return {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d,
            }
        elif self.question_type == 'true_false':
            return {
                'True': 'True',
                'False': 'False',
            }
        return {}


class UserExam(models.Model):
    user_exam_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_exams')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='user_assignments')
    assigned_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    attempts_allowed = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    class Meta:
        db_table = 'userexams'
        verbose_name = 'User Exam Assignment'
        verbose_name_plural = 'User Exam Assignments'
        unique_together = ['user', 'exam']
    
    def __str__(self):
        return f"{self.user.name} - {self.exam.exam_title}"
    
    def get_attempts_taken(self):
        return self.exam_sessions.filter(is_submitted=True).count()
    
    def can_take_exam(self):
        return (
            self.get_attempts_taken() < self.attempts_allowed and
            timezone.now() <= self.due_date
        )
    
    @property
    def status(self):
        """Calculate status based on exam sessions and conditions"""
        # Check if any attempts have been completed
        if self.exam_sessions.filter(is_submitted=True).exists():
            return 'completed'
        
        # Check if there's an active session
        active_session = self.exam_sessions.filter(is_submitted=False).first()
        if active_session:
            return 'in_progress'
        
        # Default to not started
        return 'not_started'


class ExamSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_exam = models.ForeignKey(UserExam, on_delete=models.CASCADE, related_name='exam_sessions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    session_data = models.TextField(default='{}', help_text='JSON data storing current answers')
    is_submitted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'examsessions'
        verbose_name = 'Exam Session'
        verbose_name_plural = 'Exam Sessions'
    
    def __str__(self):
        return f"{self.user.name} - {self.exam.exam_title} - {self.start_time}"
    
    def is_time_expired(self):
        """Check if exam session time has expired"""
        from django.utils import timezone
        if not self.start_time:
            return False
        
        elapsed_time = timezone.now() - self.start_time
        exam_duration_seconds = self.user_exam.exam.time_limit * 60  # Convert minutes to seconds
        return elapsed_time.total_seconds() > exam_duration_seconds
    
    def get_time_remaining(self):
        """Get remaining time in seconds"""
        from django.utils import timezone
        if not self.start_time:
            return 0
        
        elapsed_time = timezone.now() - self.start_time
        exam_duration_seconds = self.user_exam.exam.time_limit * 60
        remaining_seconds = exam_duration_seconds - elapsed_time.total_seconds()
        return max(0, int(remaining_seconds))
    
    def get_session_data(self):
        try:
            return json.loads(self.session_data) if self.session_data else {}
        except json.JSONDecodeError:
            return {}
    
    def set_session_data(self, data):
        self.session_data = json.dumps(data)
    
    def get_remaining_time_seconds(self):
        if self.is_submitted or self.end_time:
            return 0
        
        elapsed = timezone.now() - self.start_time
        total_seconds = self.exam.time_limit * 60
        remaining = total_seconds - elapsed.total_seconds()
        return max(0, int(remaining))
    
    def is_expired(self):
        return self.get_time_remaining() <= 0


class UserHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_history')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='answer_history')
    answer_given = models.CharField(max_length=10)
    is_correct = models.BooleanField()
    attempt_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'userhistory'
        verbose_name = 'User Answer History'
        verbose_name_plural = 'User Answer History'
        unique_together = ['session', 'question']
    
    def __str__(self):
        return f"{self.user.name} - Q{self.question.sort_order} - {self.answer_given}"
