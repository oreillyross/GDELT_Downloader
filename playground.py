

# Read your HTML files
with open('file1.html', 'r') as f1, open('file2.html', 'r') as f2:
    file1_content = f1.read()
    file2_content = f2.read()

# Compare the files
results = compare_html_files(file1_content, file2_content)
print_comparison_report(results)