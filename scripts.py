import os
import sys
sys.path.insert(0, os.path.abspath('../Oberon/oberon'))
import config
from core import create_json_app
from models import db, Course
app = create_json_app(config.Config)
app.app_context().push()

headers = ["Diversity Requirement 1", "Diversity Requirement 2", "Diversity Requirement 3", "Multiple Diversity Requirements", "Core Social Science", "Core Theology", "Fine Arts Requirement", "Core Social Science and Diversity", "Core Theology and Diversity", "Fine Arts and Diversity"]

# Print heading for README.md
print "#Fall 16 Core Requirements"
print "I made this list to help me pick my classes. Hope it helps! The list is categorized by section, just click on the link to get to the right section"

def linkify_header(header):
    return '- [' + header + ']' + '(#' + header.lower().replace(" ", "-") + ')'

def print_heading_links(headers):
    for header in headers:
        print linkify_header(header)

def create_course_tup(course):
    # (course.name, course.subject, course.subject_level, course.attributes)
    return (course.name, course.subject, course.subject_level, sorted([attr.name for attr in course.attributes]))

def contains_attribute(course_tup, attribute):
    return True if attribute in course_tup[3] else False

def num_diversity_reqs(course_tup):
    diversity_reqs = ['Diversity Requirement 1', 'Diversity Requirement 2', 'Diversity Requirement 3']
    return sum([contains_attribute(course_tup, attr) for attr in diversity_reqs])

def pretty_print(header_section_tuple):
    header = header_section_tuple[0]
    course_tups = header_section_tuple[1]
    print "##" + header
    print "| Course | Attributes |"
    print "| ------ | ---------- |"
    for course in course_tups:
        print "| " + course[1] + "-" + course[2] + "<br> " + course[0] + " | " + ", <br>".join(course[3]) + " |"
    print "\n\n"

def pretty_print_all(sections):
    for section in sections:
        pretty_print(section)

# list of all courses
all_courses = Course.query.all()

#list of all course tuples
course_tups = [create_course_tup(course) for course in all_courses]

diversity_1 = [ course for course in course_tups if contains_attribute(course, 'Diversity Requirement 1')]
diversity_2 = [ course for course in course_tups if contains_attribute(course, 'Diversity Requirement 2')]
diversity_3 = [ course for course in course_tups if contains_attribute(course, 'Diversity Requirement 3')]

# More than one diversity requirement
diversity_4 = [ course for course in course_tups if num_diversity_reqs(course) > 1 ]

# Core Social Science
core_ss = [ course for course in course_tups if contains_attribute(course, 'Core Social Science')]

# Core Theology
core_theo = [ course for course in course_tups if contains_attribute(course, 'Core Theology')]

 # Core Fine Arts Req
core_fine_arts = [ course for course in course_tups if contains_attribute(course, 'Fine Arts Requirement')]

# Core Social Science and diversity
core_ss_and_diversity = [ course for course in course_tups if contains_attribute(course, 'Core Social Science') and num_diversity_reqs(course) > 0]

# Core Theology and Diversity
core_theo_and_diversity = [ course for course in course_tups if contains_attribute(course, 'Core Theology') and num_diversity_reqs(course) > 0]

core_fine_arts_and_diversity = [ course for course in course_tups if contains_attribute(course, 'Fine Arts Requirement') and num_diversity_reqs(course) > 0]

sections = [diversity_1, diversity_2, diversity_3, diversity_4, core_ss, core_theo, core_fine_arts, core_ss_and_diversity, core_theo_and_diversity, core_fine_arts_and_diversity]
sections = zip(headers, sections)

print_heading_links(headers)
print " "
pretty_print_all(sections)
