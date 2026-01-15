# STRICT Django Educational Management System Requirements

## ⚠️ CRITICAL INSTRUCTIONS FOR IMPLEMENTATION

**DO NOT ADD ANY FEATURES, FIELDS, OR FUNCTIONALITY BEYOND WHAT IS EXPLICITLY SPECIFIED BELOW**

- NO marks/scores/grades in evaluation system
- NO feedback comments or text fields for evaluation
- NO additional user roles beyond DDPI, BEO, Principal (Django Groups)
- NO custom authentication system - use Django's built-in auth only
- NO notification systems
- NO email functionality  
- NO file upload capabilities for students
- NO attendance tracking
- NO fee management
- NO timetable management
- NO messaging between users
- NO profile pictures or avatars
- NO audit logs or activity tracking
- NO backup/restore features
- NO API endpoints unless explicitly required
- NO function-based views for CRUD operations
- NO multiple Django apps - single application only
- ONLY implement what is listed in these requirements
- MANDATORY: Use Django's built-in User, Group, and Permission models
- MANDATORY: Use Class-Based Views with proper mixins for ALL operations

## System Overview
Build a Django application for educational management with hierarchical structure and form-based operations.

## Organizational Hierarchy (EXACT Structure)
1. **Deputy Director of Public Instruction (DDPI)** - One per district, manages BEO accounts and talukas
2. **Block Education Officer (BEO)** - One per taluka under district, managed by DDPI, manages schools and principals
3. **Schools** - Multiple schools under each BEO/taluka, managed by BEO
4. **Principal** - One per school, managed by BEO, manages students
5. **Students** - 1st to 10th standard under each school, managed by Principal

## User Roles & Access (NO Additional Roles)

### DDPI Login Features (ONLY These)
- Manage talukas using Django forms (Create, Read, Update, Delete operations)
- Manage BEO accounts using Django forms (Create, Read, Update, Delete operations)
- Manage BEO-taluka mappings using Django forms (Create, Read, Update, Delete operations)
- Manage subjects using Django forms (Create, Read, Update, Delete operations)
- Manage assignments using Django forms with:
  - Title (text field)
  - Tasks/activities (list of strings - multiple task entries)
  - Subject selection (dropdown)
  - Class/Standard selection (1st-10th)
  - Start date (date field)
  - End date (date field)
- View hierarchical reports using filtered forms

### BEO Login Features (ONLY These)
- Manage schools using Django forms with fields (Create, Read, Update, Delete operations):
  - UDISE code (unique text field)
  - School name (text field)
  - Taluka/block name (dropdown - assigned taluka only)
  - Type: Boys only/Girls only/Co-educational (radio buttons)
  - School type (text field)
  - Location: Urban/Rural (radio buttons)
  - Medium: Kannada/English/Marathi/Urdu (dropdown)
- Manage principal accounts using Django forms (Create, Read, Update, Delete operations)
- Manage principal-school mappings using Django forms (Create, Read, Update, Delete operations)
- View reports for schools in assigned taluka using filtered forms

### Principal Login Features (ONLY These)
- Manage students using Django forms with fields (Create, Read, Update, Delete operations):
  - Name (text field)
  - STS number/enrollment number (text field)
  - Gender (radio buttons/dropdown)
  - Class/Standard (dropdown 1st-10th)
- Evaluate assignments using SINGLE PAGE interface showing:
  - Assignment title
  - List of individual tasks (from task list)
  - Table format with:
    - Student names in left column
    - Individual task columns (Task 1, Task 2, etc.)
    - Two checkboxes per cell: ✓ (SOLVED) and ✗ (UNSOLVED) - only one selectable per task per student
  - Each task is evaluated individually for each student
  - Assignment starts in "ASSIGNED" status automatically when created
- Bulk update functionality for assignment evaluation
- View reports for students in their school only

## Assignment System (EXACT Fields Only)
**Assignment Model Fields:**
- Title (CharField)
- Tasks/activities (JSONField or related model - list of task strings)
- Subject (ForeignKey)
- Class/Standard (IntegerField - 1 to 10)
- Start date (DateField)
- End date (DateField)

**Assignment Status Flow:**
- **Initial Status**: All assignments are created in "ASSIGNED" status automatically
- **Task Tracking**: Each task in the assignment is tracked individually per student
- **Principal Updates**: Principal marks each task as "SOLVED" or "UNSOLVED" for each student
- **Tabular Format**: Principal evaluates all students for one assignment in single table view

**Task Evaluation Structure:**
- Each assignment contains multiple tasks (list of strings)
- Each student gets individual task completion tracking
- Each task per student has status: SOLVED/UNSOLVED
- NO overall assignment completion - only individual task completion tracking
- Evaluation done in tabular format showing all students vs all tasks

**Task Evaluation:**
- Only SOLVED (✓) or UNSOLVED (✗) per individual task per student
- Each task in assignment is tracked separately for each student
- NO scores, marks, grades, or comments
- NO percentage calculations
- NO overall assignment completion status - only individual task completion
- NO performance metrics beyond individual task completion status

## Student Management (EXACT Fields Only)
**Student Model Fields:**
- Name (CharField)
- STS number/enrollment number (CharField)
- Gender (CharField with choices)
- Class/Standard (IntegerField - 1 to 10)
- School (ForeignKey)

**CRUD Operations:**
- Create, Read, Update, Delete operations through Django forms
- Managed by Principal for their assigned school only
**NO student login accounts required**
**NO additional student information fields**

## School Management (EXACT Fields Only)
**School Model Fields:**
- UDISE code (CharField - unique)
- School name (CharField)
- Taluka (ForeignKey)
- Type: Boys only/Girls only/Co-educational (CharField with choices)
- School type (CharField)
- Location: Urban/Rural (CharField with choices)
- Medium: Kannada/English/Marathi/Urdu (CharField with choices)

## Reporting System (EXACT Specifications)
**NO stored reports in database**
**Real-time data generation only**

**Filter Options (ONLY These):**
- Class/Standard (1st-10th)
- Taluka
- District
- School  
- Subject
- Assignment
- Date Range

**Excel Download Features:**
- Generate on-the-fly based on filters
- Include only: student names, STS numbers, gender, class, individual task completion status
- Show each task completion status separately (Task 1: SOLVED/UNSOLVED, Task 2: SOLVED/UNSOLVED, etc.)
- NO marks, grades, or detailed performance metrics
- File naming: filters + timestamp

**Access Control:**
- Principal: Own school students only
- BEO: Schools in assigned taluka only  
- DDPI: All schools in district



## Technical Requirements (EXACT Stack)
- Single Django application
- Django built-in User model and authentication system
- Django built-in Groups and Permissions for role-based access control
- User role management through Django Groups (DDPI, BEO, Principal groups)
- Django Forms for ALL user input including user management
- Tailwind CSS for styling
- Responsive design
- NO additional libraries beyond Django + Tailwind

## User Authentication & Role Management (Django Built-in System)
**Use Django's Built-in Authentication System:**
- **User Model**: Django's default User model (username, password, email, etc.)
- **Groups**: Create 3 groups - DDPI, BEO, Principal
- **Role Assignment**: Assign users to appropriate groups
- **Permission Management**: Use Django's built-in permission system

**User Management Forms Required:**
- **User Creation Forms**: Create users and assign to groups (DDPI creates BEOs, BEO creates Principals)
- **User Update Forms**: Update user information and group assignments
- **User Delete Forms**: Deactivate/delete user accounts
- **Group Management Forms**: Assign/remove users from groups
- **Profile Forms**: Additional profile information (district assignment, taluka assignment, school assignment)

**User Profile Extensions:**
- **DDPI Profile**: District assignment field
- **BEO Profile**: Taluka assignment field (linked to DDPI's district)
- **Principal Profile**: School assignment field (linked to BEO's taluka)

## Django Implementation Requirements (EXACT Architecture)
**MANDATORY: Use Django Class-Based Views (CBVs) with Proper Mixins**

### View Architecture Requirements:
- **ALL CRUD operations MUST use Class-Based Views**
- **Use Django Generic Views**: CreateView, UpdateView, DeleteView, ListView, DetailView
- **Use Permission Mixins**: LoginRequiredMixin, UserPassesTestMixin for role-based access
- **Use Form Mixins**: FormMixin, ModelFormMixin for form handling
- **Custom Mixins**: Create role-based mixins (DDPIMixin, BEOMixin, PrincipalMixin) for access control

### Required CBV Implementation:
```python
# Example structure - MUST follow this pattern
class DDPIRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='DDPI').exists()

class BEORequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='BEO').exists()

class PrincipalRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Principal').exists()

class ManageTalukaCreateView(LoginRequiredMixin, DDPIRequiredMixin, CreateView):
    # Taluka creation logic

class ManageTalukaUpdateView(LoginRequiredMixin, DDPIRequiredMixin, UpdateView):
    # Taluka update logic

class ManageTalukaDeleteView(LoginRequiredMixin, DDPIRequiredMixin, DeleteView):
    # Taluka deletion logic

class ManageTalukaListView(LoginRequiredMixin, DDPIRequiredMixin, ListView):
    # Taluka listing logic
```

### Form Integration:
- Use get_form_class() method in CBVs
- Use form_valid() and form_invalid() methods for form processing
- Use get_context_data() for additional context
- Use get_queryset() for data filtering based on user roles

### Access Control Implementation:
- Each CBV MUST include appropriate permission mixins
- Role-based queryset filtering in get_queryset() method
- Hierarchical data access control through custom mixins
- NO function-based views allowed for CRUD operations

## UI/UX Requirements (EXACT Specifications)
- Tailwind CSS styling only
- Django forms for all operations
- Responsive design (desktop, tablet, mobile)
- Clean navigation based on user roles
- Form validation with error messages
- NO complex animations or advanced UI components
- NO dashboards beyond basic filtered views

## Database Models (EXACT Fields)

### Django Built-in Models (Use As-Is)
- **User**: Django's default User model
- **Group**: Django's default Group model (DDPI, BEO, Principal groups)
- **Permission**: Django's default Permission model

### Profile Extensions (Additional Fields)
- **DDPI Profile**: 
  - User (OneToOneField to User)
  - District (ForeignKey)
- **BEO Profile**:
  - User (OneToOneField to User)  
  - Taluka (ForeignKey)
- **Principal Profile**:
  - User (OneToOneField to User)
  - School (ForeignKey)

### Core Models (NO Additional Fields)
- District (CharField)
- Taluka (CharField, ForeignKey to District)
- School (UDISE code, name, taluka, type, school_type, location, medium)
- Subject (CharField)
- Student (Name, STS number, Gender, Class/Standard, School)
- Assignment (Title, Tasks list, Subject, Class, Start/End dates)
- Task Evaluation (Student + Assignment + Task + Solved/Unsolved status)

## Form Requirements (EXACT Implementation)
- Use Django ModelForms with Class-Based Views
- Use Django FormSets for bulk evaluation with appropriate CBV mixins
- Custom validation only for business rules implemented in form_valid() methods
- NO complex form widgets beyond standard HTML inputs
- NO JavaScript beyond basic form interactions
- Integrate forms with CBV lifecycle methods (get_form_class, form_valid, form_invalid)
- Use get_context_data() in CBVs for additional form context

## Security & Access (EXACT Requirements)
- Django built-in authentication system
- Django Groups for role-based access control (DDPI, BEO, Principal groups)
- Django Permissions for fine-grained access control
- Role-based view restrictions using Django's @user_passes_test and UserPassesTestMixin
- Hierarchical data access based on profile assignments (district, taluka, school)
- Group membership validation in CBV mixins
- NO additional security features beyond Django's built-in system

## Performance (EXACT Requirements)
- Basic database optimization
- Efficient queries for reports
- NO caching mechanisms
- NO advanced performance features

---

## FINAL REMINDER
**IMPLEMENT ONLY WHAT IS EXPLICITLY LISTED ABOVE**
**NO ADDITIONAL FEATURES, FIELDS, OR FUNCTIONALITY**
**CLIENT-APPROVED REQUIREMENTS ONLY**