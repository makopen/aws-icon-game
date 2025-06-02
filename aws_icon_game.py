import pygame
import random
import time
import os
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cyberpunk Colors
NEON_PINK = (255, 0, 128)
NEON_BLUE = (0, 195, 255)
NEON_GREEN = (0, 255, 128)
NEON_YELLOW = (255, 255, 0)
DARK_PURPLE = (25, 0, 51)
DARK_BLUE = (5, 10, 20)
BLACK = (10, 10, 15)
GRAY = (50, 50, 60)
LIGHT_GRAY = (100, 100, 120)
WHITE = (255, 255, 255)

# Game settings
TOTAL_QUESTIONS = 10
REVEAL_STEPS = 40  # Increased for smoother reveal
ICON_SIZE = 128    # Larger icon size for better visibility

class AWSIconGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('AWS Icon Guessing Game - Cyberpunk Edition')
        self.clock = pygame.time.Clock()
        
        # Load fonts - use system fonts that look cyberpunk
        try:
            self.font_large = pygame.font.SysFont('Arial', 40, bold=True)
            self.font_medium = pygame.font.SysFont('Arial', 28)
            self.font_small = pygame.font.SysFont('Arial', 22)
            self.font_tiny = pygame.font.SysFont('Arial', 16)
        except:
            # Fallback to default font if custom fonts fail
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 28)
            self.font_tiny = pygame.font.Font(None, 20)
        
        # Load AWS service data
        self.aws_services = [
            {"name": "Amazon EC2", "icon": "ec2.png", "description": "Virtual servers in the cloud"},
            {"name": "Amazon S3", "icon": "s3.png", "description": "Scalable storage in the cloud"},
            {"name": "Amazon RDS", "icon": "rds.png", "description": "Managed relational database service"},
            {"name": "AWS Lambda", "icon": "lambda.png", "description": "Run code without thinking about servers"},
            {"name": "Amazon DynamoDB", "icon": "dynamodb.png", "description": "Managed NoSQL database"},
            {"name": "Amazon CloudWatch", "icon": "cloudwatch.png", "description": "Monitor resources and applications"},
            {"name": "AWS IAM", "icon": "iam.png", "description": "Manage access to AWS services"},
            {"name": "Amazon VPC", "icon": "vpc.png", "description": "Isolated cloud resources"},
            {"name": "Amazon SNS", "icon": "sns.png", "description": "Pub/sub messaging service"},
            {"name": "Amazon SQS", "icon": "sqs.png", "description": "Message queuing service"},
            {"name": "AWS CloudFormation", "icon": "cloudformation.png", "description": "Create and manage resources with templates"},
            {"name": "Amazon ECS", "icon": "ecs.png", "description": "Run containerized applications"},
            {"name": "Amazon EKS", "icon": "eks.png", "description": "Managed Kubernetes service"},
            {"name": "AWS Fargate", "icon": "fargate.png", "description": "Serverless compute for containers"},
            {"name": "Amazon API Gateway", "icon": "apigateway.png", "description": "Create, publish, and manage APIs"},
            {"name": "Amazon Route 53", "icon": "route53.png", "description": "Scalable DNS and domain registration"},
            {"name": "AWS Elastic Beanstalk", "icon": "elasticbeanstalk.png", "description": "Deploy and scale web applications"},
            {"name": "AWS CodePipeline", "icon": "codepipeline.png", "description": "Continuous delivery service"},
            {"name": "AWS CodeBuild", "icon": "codebuild.png", "description": "Build and test code"},
            {"name": "AWS CodeCommit", "icon": "codecommit.png", "description": "Store code in private Git repositories"},
            {"name": "Amazon Athena", "icon": "athena.png", "description": "Query data in S3 using SQL"},
            {"name": "AWS Glue", "icon": "glue.png", "description": "Prepare and load data"},
            {"name": "Amazon Redshift", "icon": "redshift.png", "description": "Fast, simple, cost-effective data warehousing"},
            {"name": "Amazon Aurora", "icon": "aurora.png", "description": "MySQL and PostgreSQL compatible database"},
            {"name": "Amazon EventBridge", "icon": "eventbridge.png", "description": "Serverless event bus"},
            {"name": "AWS Step Functions", "icon": "step-functions.png", "description": "Coordinate distributed applications"},
            {"name": "AWS Secrets Manager", "icon": "secrets-manager.png", "description": "Rotate, manage, and retrieve secrets"},
            {"name": "Amazon Cognito", "icon": "cognito.png", "description": "User identity and data synchronization"},
            {"name": "Amazon GuardDuty", "icon": "guardduty.png", "description": "Intelligent threat detection"},
            {"name": "AWS WAF", "icon": "waf.png", "description": "Filter malicious web traffic"}
        ]
        
        self.current_question = 0
        self.correct_answers = 0
        self.start_time = 0
        self.total_time = 0
        self.questions = []
        self.current_reveal_step = 0
        self.game_state = "start"  # start, playing, result, review
        self.user_answers = []  # Store user's answers for review
        self.icon_cache = {}  # Cache for resized icons
        
        # Create icons directory if it doesn't exist
        if not os.path.exists('icons'):
            os.makedirs('icons')
            print("Created 'icons' directory. Please place AWS service icons in this folder.")
    
    def prepare_questions(self):
        # Randomly select 10 services for the quiz
        selected_services = random.sample(self.aws_services, TOTAL_QUESTIONS)
        self.questions = []
        self.user_answers = []
        
        for service in selected_services:
            # For each question, create 3 wrong options
            options = [service["name"]]
            other_services = [s["name"] for s in self.aws_services if s["name"] != service["name"]]
            wrong_options = random.sample(other_services, 3)
            options.extend(wrong_options)
            random.shuffle(options)
            
            self.questions.append({
                "service": service,
                "options": options,
                "correct_option": options.index(service["name"])
            })
            
            # Initialize user answers with -1 (not answered)
            self.user_answers.append(-1)
    
    def load_and_resize_icon(self, icon_path):
        """Load an icon and resize it to the standard size"""
        if icon_path in self.icon_cache:
            return self.icon_cache[icon_path]
            
        try:
            # Load the original icon
            icon = pygame.image.load(icon_path)
            
            # Create a new surface with the standard size
            resized_icon = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
            resized_icon.fill((0, 0, 0, 0))  # Transparent background
            
            # Calculate scaling to fit within the standard size
            orig_width, orig_height = icon.get_size()
            scale_factor = min(ICON_SIZE / orig_width, ICON_SIZE / orig_height)
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            
            # Scale the icon
            if new_width > 0 and new_height > 0:  # Ensure valid dimensions
                scaled_icon = pygame.transform.smoothscale(icon, (new_width, new_height))
                
                # Center the scaled icon
                x_offset = (ICON_SIZE - new_width) // 2
                y_offset = (ICON_SIZE - new_height) // 2
                resized_icon.blit(scaled_icon, (x_offset, y_offset))
            
            # Cache the resized icon
            self.icon_cache[icon_path] = resized_icon
            return resized_icon
            
        except pygame.error as e:
            print(f"Error loading icon {icon_path}: {e}")
            # Return a placeholder if the icon can't be loaded
            placeholder = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
            placeholder.fill((200, 200, 200, 255))
            return placeholder

    def draw_text(self, text, font, color, x, y, centered=True, glow=False, glow_color=None, glow_amount=2):
        """Draw text with optional cyberpunk glow effect"""
        if glow:
            if glow_color is None:
                glow_color = NEON_BLUE
            
            # Draw glow effect
            for offset in range(1, glow_amount + 1):
                glow_surface = font.render(text, True, glow_color)
                if centered:
                    glow_rect = glow_surface.get_rect(center=(x, y))
                else:
                    glow_rect = glow_surface.get_rect(topleft=(x, y))
                
                # Adjust position for glow effect
                glow_rect.x += random.randint(-1, 1)
                glow_rect.y += random.randint(-1, 1)
                
                # Reduce alpha for glow
                glow_surface.set_alpha(150 // offset)
                self.screen.blit(glow_surface, glow_rect)
        
        # Draw main text
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_cyberpunk_button(self, text, x, y, width, height, primary=True):
        """Draw a button in cyberpunk style"""
        mouse_pos = pygame.mouse.get_pos()
        hover = x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height
        
        # Button colors based on primary/secondary and hover state
        if primary:
            bg_color = NEON_PINK if not hover else (255, 50, 150)
            border_color = NEON_BLUE
            text_color = BLACK
        else:
            bg_color = DARK_BLUE if not hover else GRAY
            border_color = NEON_GREEN
            text_color = NEON_GREEN
        
        # Draw button with angled corners
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, rect)
        
        # Draw border with glitch effect
        if hover:
            # Glitch effect on hover
            for _ in range(3):
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(-2, 2)
                border_rect = pygame.Rect(x + offset_x, y + offset_y, width, height)
                pygame.draw.rect(self.screen, border_color, border_rect, 2)
        else:
            pygame.draw.rect(self.screen, border_color, rect, 2)
        
        # Add diagonal lines in corners for cyberpunk feel
        pygame.draw.line(self.screen, border_color, (x, y), (x + 10, y + 10), 1)
        pygame.draw.line(self.screen, border_color, (x + width, y), (x + width - 10, y + 10), 1)
        pygame.draw.line(self.screen, border_color, (x, y + height), (x + 10, y + height - 10), 1)
        pygame.draw.line(self.screen, border_color, (x + width, y + height), (x + width - 10, y + height - 10), 1)
        
        # Draw text with glow effect if hovering
        self.draw_text(text, self.font_medium, text_color, x + width/2, y + height/2, glow=hover, glow_color=NEON_BLUE)
        
        return hover
    
    def draw_cyberpunk_card(self, x, y, width, height):
        """Draw a card in cyberpunk style"""
        # Draw card background
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, DARK_BLUE, card_rect)
        
        # Draw border with neon effect
        pygame.draw.rect(self.screen, NEON_BLUE, card_rect, 2)
        
        # Add diagonal lines in corners for cyberpunk feel
        line_length = 20
        pygame.draw.line(self.screen, NEON_PINK, (x, y), (x + line_length, y), 2)
        pygame.draw.line(self.screen, NEON_PINK, (x, y), (x, y + line_length), 2)
        
        pygame.draw.line(self.screen, NEON_PINK, (x + width, y), (x + width - line_length, y), 2)
        pygame.draw.line(self.screen, NEON_PINK, (x + width, y), (x + width, y + line_length), 2)
        
        pygame.draw.line(self.screen, NEON_PINK, (x, y + height), (x + line_length, y + height), 2)
        pygame.draw.line(self.screen, NEON_PINK, (x, y + height), (x, y + height - line_length), 2)
        
        pygame.draw.line(self.screen, NEON_PINK, (x + width, y + height), (x + width - line_length, y + height), 2)
        pygame.draw.line(self.screen, NEON_PINK, (x + width, y + height), (x + width, y + height - line_length), 2)
        
        # Add some random "circuit" lines for decoration
        for _ in range(5):
            start_x = random.randint(x + 10, x + width - 10)
            start_y = random.randint(y + 10, y + height - 10)
            end_x = start_x + random.randint(-30, 30)
            end_y = start_y + random.randint(-30, 30)
            
            # Keep lines within the card
            end_x = max(x + 5, min(x + width - 5, end_x))
            end_y = max(y + 5, min(y + height - 5, end_y))
            
            pygame.draw.line(self.screen, NEON_GREEN, (start_x, start_y), (end_x, end_y), 1)
    
    def draw_progress_bar(self, x, y, width, height, progress):
        """Draw a progress bar in cyberpunk style"""
        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, DARK_BLUE, bg_rect)
        pygame.draw.rect(self.screen, NEON_BLUE, bg_rect, 1)
        
        # Progress
        if progress > 0:
            progress_width = int(width * progress)
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(self.screen, NEON_PINK, progress_rect)
            
            # Add scan line effect
            for line_y in range(y, y + height, 2):
                pygame.draw.line(self.screen, NEON_BLUE, (x, line_y), (x + progress_width, line_y), 1)
    
    def draw_cyberpunk_background(self):
        """Draw a cyberpunk-style grid background"""
        # Draw horizontal grid lines
        for y in range(0, SCREEN_HEIGHT, 20):
            alpha = max(50, 150 - abs(y - SCREEN_HEIGHT/2))
            line_color = (NEON_BLUE[0], NEON_BLUE[1], NEON_BLUE[2], alpha)
            pygame.draw.line(self.screen, line_color, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw vertical grid lines
        for x in range(0, SCREEN_WIDTH, 20):
            alpha = max(50, 150 - abs(x - SCREEN_WIDTH/2))
            line_color = (NEON_BLUE[0], NEON_BLUE[1], NEON_BLUE[2], alpha)
            pygame.draw.line(self.screen, line_color, (x, 0), (x, SCREEN_HEIGHT), 1)
    
    def draw_start_screen(self):
        # Background with grid effect
        self.screen.fill(BLACK)
        self.draw_cyberpunk_background()
        
        # Header
        self.draw_text("AWS ICON GUESSING GAME", self.font_large, NEON_PINK, SCREEN_WIDTH/2, 80, glow=True)
        self.draw_text("CYBERPUNK EDITION", self.font_medium, NEON_BLUE, SCREEN_WIDTH/2, 120, glow=True)
        
        # Main content card
        self.draw_cyberpunk_card(SCREEN_WIDTH/2 - 300, 160, 600, 350)
        
        # Game description
        self.draw_text("TEST YOUR KNOWLEDGE OF AWS SERVICES", self.font_medium, NEON_GREEN, SCREEN_WIDTH/2, 200)
        self.draw_text("• Icons will be revealed from top to bottom", self.font_small, NEON_BLUE, SCREEN_WIDTH/2, 250)
        self.draw_text("• Choose the correct service name from 4 options", self.font_small, NEON_BLUE, SCREEN_WIDTH/2, 290)
        self.draw_text("• 10 questions total from 30 AWS services", self.font_small, NEON_BLUE, SCREEN_WIDTH/2, 330)
        self.draw_text("• See your AWS knowledge level at the end", self.font_small, NEON_BLUE, SCREEN_WIDTH/2, 370)
        
        # Start button
        start_clicked = self.draw_cyberpunk_button("START GAME", SCREEN_WIDTH/2 - 100, 450, 200, 60, primary=True)
        
        # Footer
        self.draw_text("© 2077 NETRUNNER SYSTEMS", self.font_tiny, NEON_YELLOW, SCREEN_WIDTH/2, SCREEN_HEIGHT - 20)
        
        # Add some random "glitch" effects
        if random.random() < 0.05:  # 5% chance each frame
            glitch_x = random.randint(0, SCREEN_WIDTH)
            glitch_y = random.randint(0, SCREEN_HEIGHT)
            glitch_width = random.randint(10, 100)
            glitch_height = random.randint(2, 10)
            pygame.draw.rect(self.screen, NEON_PINK, (glitch_x, glitch_y, glitch_width, glitch_height))
        
        return start_clicked

    def draw_game_screen(self):
        # Background with grid effect
        self.screen.fill(BLACK)
        self.draw_cyberpunk_background()
        
        # Header
        self.draw_text(f"QUESTION {self.current_question + 1}/{TOTAL_QUESTIONS}", 
                      self.font_medium, NEON_YELLOW, SCREEN_WIDTH/2, 30, glow=True)
        
        # Main content card
        self.draw_cyberpunk_card(SCREEN_WIDTH/2 - 250, 60, 500, 460)
        
        # Progress bar
        progress = self.current_question / TOTAL_QUESTIONS
        self.draw_progress_bar(SCREEN_WIDTH/2 - 200, 80, 400, 10, progress)
        
        # Load and display the icon with progressive reveal from top to bottom
        question = self.questions[self.current_question]
        icon_path = os.path.join('icons', question["service"]["icon"])
        
        try:
            # Load and resize the icon
            icon = self.load_and_resize_icon(icon_path)
            icon_rect = icon.get_rect(center=(SCREEN_WIDTH/2, 200))
            
            # Calculate reveal percentage (0 to 1)
            reveal_percentage = max(0, min(1, self.current_reveal_step / REVEAL_STEPS))
            
            # Create a white background for the icon area
            bg_rect = pygame.Rect(icon_rect.left, icon_rect.top, icon_rect.width, icon_rect.height)
            pygame.draw.rect(self.screen, WHITE, bg_rect)
            
            # Create a copy of the icon to work with
            display_icon = pygame.Surface((icon.get_width(), icon.get_height()), pygame.SRCALPHA)
            display_icon.fill((0, 0, 0, 0))  # Start with transparent
            
            # Reveal from top to bottom - simple approach
            reveal_height = int(icon.get_height() * reveal_percentage)
            if reveal_height > 0:
                # Copy the visible portion of the icon
                display_icon.blit(icon, (0, 0), (0, 0, icon.get_width(), reveal_height))
            
            # Draw the partially revealed icon
            self.screen.blit(display_icon, icon_rect)
            
            # Draw a simple border around the icon area
            pygame.draw.rect(self.screen, NEON_BLUE, icon_rect, 1)
            
        except Exception as e:
            print(f"Error displaying icon: {e}")
            self.draw_text("ICON NOT FOUND", self.font_medium, NEON_PINK, SCREEN_WIDTH/2, 200)
        
        # Display options
        option_clicked = -1
        for i, option in enumerate(question["options"]):
            y_pos = 320 + i * 50
            if self.draw_cyberpunk_button(option, SCREEN_WIDTH/2 - 150, y_pos, 300, 40, primary=False):
                option_clicked = i
        
        # Add some random "glitch" effects (but not over the icon area)
        if random.random() < 0.03:  # 3% chance each frame
            glitch_x = random.randint(0, SCREEN_WIDTH)
            glitch_y = random.randint(0, SCREEN_HEIGHT)
            
            # Make sure glitch doesn't overlap with icon
            if not (icon_rect.left < glitch_x < icon_rect.right and 
                   icon_rect.top < glitch_y < icon_rect.bottom):
                glitch_width = random.randint(10, 100)
                glitch_height = random.randint(2, 10)
                pygame.draw.rect(self.screen, NEON_PINK, (glitch_x, glitch_y, glitch_width, glitch_height))
        
        return option_clicked
    
    def draw_result_screen(self):
        # Background with grid effect
        self.screen.fill(BLACK)
        self.draw_cyberpunk_background()
        
        # Header
        self.draw_text("GAME RESULTS", self.font_large, NEON_PINK, SCREEN_WIDTH/2, 60, glow=True)
        
        # Main content card
        self.draw_cyberpunk_card(SCREEN_WIDTH/2 - 250, 100, 500, 400)
        
        # Results
        self.draw_text("YOUR AWS KNOWLEDGE LEVEL", self.font_medium, NEON_GREEN, SCREEN_WIDTH/2, 140)
        
        # Determine level based on score and time - stricter criteria
        level = "BEGINNER"
        level_color = GRAY
        if self.correct_answers == TOTAL_QUESTIONS:  # 10問全問正解
            if self.total_time < 30:  # 30秒以内
                level = "AWS EXPERT"
                level_color = NEON_BLUE
            elif self.total_time < 60:  # 60秒以内
                level = "AWS PROFESSIONAL"
                level_color = NEON_BLUE
            else:
                level = "AWS ASSOCIATE"
                level_color = NEON_GREEN
        elif self.correct_answers >= 9:  # 9問以上正解
            if self.total_time < 60:
                level = "AWS PROFESSIONAL"
                level_color = NEON_BLUE
            else:
                level = "AWS ASSOCIATE"
                level_color = NEON_GREEN
        elif self.correct_answers >= 8:  # 8問以上正解
            if self.total_time < 90:
                level = "AWS ASSOCIATE"
                level_color = NEON_GREEN
            else:
                level = "AWS PRACTITIONER"
                level_color = NEON_GREEN
        elif self.correct_answers >= 6:  # 6問以上正解
            level = "AWS PRACTITIONER"
            level_color = NEON_GREEN
        
        # Draw level badge with cyberpunk style
        badge_rect = pygame.Rect(SCREEN_WIDTH/2 - 150, 170, 300, 60)
        pygame.draw.rect(self.screen, DARK_BLUE, badge_rect)
        pygame.draw.rect(self.screen, level_color, badge_rect, 2)
        
        # Add diagonal lines in corners for cyberpunk feel
        line_length = 10
        pygame.draw.line(self.screen, level_color, (badge_rect.left, badge_rect.top), 
                        (badge_rect.left + line_length, badge_rect.top + line_length), 2)
        pygame.draw.line(self.screen, level_color, (badge_rect.right, badge_rect.top), 
                        (badge_rect.right - line_length, badge_rect.top + line_length), 2)
        pygame.draw.line(self.screen, level_color, (badge_rect.left, badge_rect.bottom), 
                        (badge_rect.left + line_length, badge_rect.bottom - line_length), 2)
        pygame.draw.line(self.screen, level_color, (badge_rect.right, badge_rect.bottom), 
                        (badge_rect.right - line_length, badge_rect.bottom - line_length), 2)
        
        self.draw_text(level, self.font_large, level_color, SCREEN_WIDTH/2, 200, glow=True)
        
        # Draw score details
        self.draw_text(f"CORRECT ANSWERS: {self.correct_answers}/{TOTAL_QUESTIONS}", 
                      self.font_medium, NEON_YELLOW, SCREEN_WIDTH/2, 270)
        self.draw_text(f"TOTAL TIME: {self.total_time:.1f} SECONDS", 
                      self.font_medium, NEON_YELLOW, SCREEN_WIDTH/2, 310)
        
        # Add Review Answers button
        review_clicked = self.draw_cyberpunk_button("REVIEW ANSWERS", SCREEN_WIDTH/2 - 150, 360, 300, 50, primary=False)
        
        # Add Play Again button
        restart_clicked = self.draw_cyberpunk_button("PLAY AGAIN", SCREEN_WIDTH/2 - 100, 430, 200, 50, primary=True)
        
        # Add some random "glitch" effects
        if random.random() < 0.05:  # 5% chance each frame
            glitch_x = random.randint(0, SCREEN_WIDTH)
            glitch_y = random.randint(0, SCREEN_HEIGHT)
            glitch_width = random.randint(10, 100)
            glitch_height = random.randint(2, 10)
            pygame.draw.rect(self.screen, NEON_PINK, (glitch_x, glitch_y, glitch_width, glitch_height))
        
        return restart_clicked, review_clicked

    def draw_review_screen(self):
        # Background with grid effect
        self.screen.fill(BLACK)
        self.draw_cyberpunk_background()
        
        # Header
        self.draw_text("ANSWER REVIEW", self.font_large, NEON_BLUE, SCREEN_WIDTH/2, 40, glow=True)
        
        # Main content card
        self.draw_cyberpunk_card(SCREEN_WIDTH/2 - 300, 80, 600, 440)
        
        # Display current question number
        self.draw_text(f"QUESTION {self.current_question + 1}/{TOTAL_QUESTIONS}", 
                      self.font_medium, NEON_YELLOW, SCREEN_WIDTH/2, 110)
        
        # Get the current question data
        question = self.questions[self.current_question]
        service = question["service"]
        correct_option = question["correct_option"]
        user_answer = self.user_answers[self.current_question]
        
        # Display the service name
        self.draw_text(f"{service['name']}", self.font_medium, NEON_PINK, SCREEN_WIDTH/2, 150, glow=True)
        
        # Display the icon with white background
        icon_path = os.path.join('icons', service["icon"])
        try:
            icon = self.load_and_resize_icon(icon_path)
            icon_rect = icon.get_rect(center=(SCREEN_WIDTH/2, 220))
            
            # Draw white background for icon
            bg_rect = pygame.Rect(icon_rect.left, icon_rect.top, icon_rect.width, icon_rect.height)
            pygame.draw.rect(self.screen, WHITE, bg_rect)
            
            # Draw the icon
            self.screen.blit(icon, icon_rect)
            
            # Draw a simple border around the icon
            pygame.draw.rect(self.screen, NEON_BLUE, icon_rect, 1)
                
        except pygame.error:
            self.draw_text("ICON NOT FOUND", self.font_medium, NEON_PINK, SCREEN_WIDTH/2, 220)
        
        # Display the description
        description_lines = self.wrap_text(service["description"], self.font_small, 500)
        for i, line in enumerate(description_lines):
            self.draw_text(line, self.font_small, NEON_GREEN, SCREEN_WIDTH/2, 300 + i * 30)
        
        # Display if the user was correct
        if user_answer == correct_option:
            result_text = "YOUR ANSWER: CORRECT!"
            result_color = NEON_GREEN
        else:
            result_text = f"YOUR ANSWER: {question['options'][user_answer]} (INCORRECT)"
            result_color = NEON_PINK
            
            # Show the correct answer
            self.draw_text(f"CORRECT ANSWER: {question['options'][correct_option]}", 
                          self.font_medium, NEON_GREEN, SCREEN_WIDTH/2, 350, glow=True)
        
        self.draw_text(result_text, self.font_medium, result_color, SCREEN_WIDTH/2, 380)
        
        # Navigation buttons
        prev_clicked = False
        next_clicked = False
        back_clicked = False
        
        # Navigation bar
        nav_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, DARK_BLUE, nav_rect)
        pygame.draw.line(self.screen, NEON_BLUE, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 1)
        
        if self.current_question > 0:
            prev_clicked = self.draw_cyberpunk_button("PREVIOUS", 100, SCREEN_HEIGHT - 60, 150, 40, primary=False)
        
        if self.current_question < TOTAL_QUESTIONS - 1:
            next_clicked = self.draw_cyberpunk_button("NEXT", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60, 150, 40, primary=False)
        
        back_clicked = self.draw_cyberpunk_button("BACK TO RESULTS", SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 60, 200, 40, primary=True)
        
        # Add some random "glitch" effects (but not over the icon)
        if random.random() < 0.03:  # 3% chance each frame
            glitch_x = random.randint(0, SCREEN_WIDTH)
            glitch_y = random.randint(0, SCREEN_HEIGHT)
            
            # Make sure glitch doesn't overlap with icon
            if not (icon_rect.left < glitch_x < icon_rect.right and 
                   icon_rect.top < glitch_y < icon_rect.bottom):
                glitch_width = random.randint(10, 100)
                glitch_height = random.randint(2, 10)
                pygame.draw.rect(self.screen, NEON_PINK, (glitch_x, glitch_y, glitch_width, glitch_height))
        
        return prev_clicked, next_clicked, back_clicked
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                # Start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.game_state == "start":
                            if self.draw_start_screen():
                                self.prepare_questions()
                                self.current_question = 0
                                self.correct_answers = 0
                                self.start_time = time.time()
                                self.current_reveal_step = 0  # Reset reveal step
                                self.game_state = "playing"
                        
                        elif self.game_state == "playing":
                            option_clicked = self.draw_game_screen()
                            if option_clicked != -1:
                                # Store the user's answer
                                self.user_answers[self.current_question] = option_clicked
                                
                                if option_clicked == self.questions[self.current_question]["correct_option"]:
                                    self.correct_answers += 1
                                
                                self.current_question += 1
                                self.current_reveal_step = 0  # Reset reveal step for next question
                                
                                if self.current_question >= TOTAL_QUESTIONS:
                                    self.total_time = time.time() - self.start_time
                                    self.game_state = "result"
                        
                        elif self.game_state == "result":
                            restart_clicked, review_clicked = self.draw_result_screen()
                            if restart_clicked:
                                self.game_state = "start"
                            elif review_clicked:
                                self.current_question = 0
                                self.game_state = "review"
                        
                        elif self.game_state == "review":
                            prev_clicked, next_clicked, back_clicked = self.draw_review_screen()
                            if prev_clicked and self.current_question > 0:
                                self.current_question -= 1
                            elif next_clicked and self.current_question < TOTAL_QUESTIONS - 1:
                                self.current_question += 1
                            elif back_clicked:
                                self.game_state = "result"
            
            if self.game_state == "start":
                self.draw_start_screen()
            elif self.game_state == "playing":
                self.draw_game_screen()
                # Gradually reveal the icon
                if self.current_reveal_step < REVEAL_STEPS:
                    self.current_reveal_step += 0.2  # Increased speed for testing
            elif self.game_state == "result":
                self.draw_result_screen()
            elif self.game_state == "review":
                self.draw_review_screen()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    game = AWSIconGame()
    game.run()

