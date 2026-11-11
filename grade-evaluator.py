import csv
import sys
import os

def load_csv_data():
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                group_val = row['group'].strip().lower()
                # Normalize FA/Formative and SA/Summative
                if group_val in ['fa', 'formative']:
                    normalized_group = 'formative'
                elif group_val in ['sa', 'summative']:
                    normalized_group = 'summative'
                else:
                    normalized_group = group_val

                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': normalized_group,
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    print("\n--- Processing Grades ---")
    if not data:
        print("Error: The CSV file is empty.")
        sys.exit(1)
    
    for item in data:
        if not (0.0 <= item['score'] <= 100.0):
            print(f"Error: Invalid score '{item['score']}' for assignment '{item['assignment']}'. Scores must be between 0 and 100.")
            sys.exit(1)
               
    total_weight = sum(item['weight'] for item in data)
    summative_weight = sum(item['weight'] for item in data if item['group'] == 'summative')
    formative_weight = sum(item['weight'] for item in data if item['group'] == 'formative')
    
    if abs(total_weight - 100.0) > 1e-5:
        print(f"Error: Total weight is {total_weight}, but it must equal exactly 100.")
        sys.exit(1)
    if abs(summative_weight - 40.0) > 1e-5:
        print(f"Error: Summative weight sum is {summative_weight}, but it must equal exactly 40.")
        sys.exit(1)
    if abs(formative_weight - 60.0) > 1e-5:
        print(f"Error: Formative weight sum is {formative_weight}, but it must equal exactly 60.")
        sys.exit(1)
           
    total_grade = sum(item['score'] * (item['weight'] / 100.0) for item in data)
    gpa = (total_grade / 100.0) * 5.0
       
    formative_items = [item for item in data if item['group'] == 'formative']
    summative_items = [item for item in data if item['group'] == 'summative']
    
    formative_weighted_sum = sum(item['score'] * item['weight'] for item in formative_items)
    formative_percentage = formative_weighted_sum / formative_weight if formative_weight > 0 else 0
    
    summative_weighted_sum = sum(item['score'] * item['weight'] for item in summative_items)
    summative_percentage = summative_weighted_sum / summative_weight if summative_weight > 0 else 0
    
    # Pass rule: >= 50% in BOTH categories
    passed_categories = formative_percentage >= 50.0 and summative_percentage >= 50.0
    status = "PASSED" if passed_categories else "FAILED"
       
    failed_formatives = [item for item in formative_items if item['score'] < 50.0]
    resubmission_targets = []
    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        resubmission_targets = [item for item in failed_formatives if abs(item['weight'] - max_weight) < 1e-5]
           
    print(f"Final Weighted Grade: {total_grade:.2f}%")
    print(f"Final GPA: {gpa:.3f} / 5.00")
    print(f"Formative Category Score: {formative_percentage:.2f}% ({'PASS' if formative_percentage >= 50 else 'FAIL'})")
    print(f"Summative Category Score: {summative_percentage:.2f}% ({'PASS' if summative_percentage >= 50 else 'FAIL'})")
    print(f"Status: {status}")
       
    if failed_formatives:
        print("Available for resubmission:")
        for target in resubmission_targets:
            print(f" - {target['assignment']}")
    else:
        print("Available for resubmission: None")

if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
