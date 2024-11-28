import difflib
from collections import Counter

from bs4 import BeautifulSoup


def compare_html_files(file1_content, file2_content):
    """
    Compare two HTML files to identify repeated content and subsets.

    Args:
        file1_content (str): Content of first HTML file
        file2_content (str): Content of second HTML file

    Returns:
        dict: Comparison results including duplicates and subset information
    """
    # Parse HTML content
    soup1 = BeautifulSoup(file1_content, 'html.parser')
    soup2 = BeautifulSoup(file2_content, 'html.parser')

    # Extract text content
    text1 = soup1.get_text(separator=' ').strip()
    text2 = soup2.get_text(separator=' ').strip()

    # Compare text content
    diff = difflib.SequenceMatcher(None, text1, text2)
    ratio = diff.ratio()

    # Find repeated elements in both files
    elements1 = [str(tag) for tag in soup1.find_all()]
    elements2 = [str(tag) for tag in soup2.find_all()]

    counter1 = Counter(elements1)
    counter2 = Counter(elements2)

    # Find duplicates within each file
    duplicates1 = {elem: count for elem, count in counter1.items() if count > 1}
    duplicates2 = {elem: count for elem, count in counter2.items() if count > 1}

    # Check if one file is a subset of the other
    is_subset = False
    subset_direction = None
    if set(elements1).issubset(set(elements2)):
        is_subset = True
        subset_direction = "File 1 is a subset of File 2"
    elif set(elements2).issubset(set(elements1)):
        is_subset = True
        subset_direction = "File 2 is a subset of File 1"

    # Generate detailed comparison report
    results = {
        "similarity_ratio": ratio,
        "is_subset": is_subset,
        "subset_direction": subset_direction,
        "file1_duplicates": duplicates1,
        "file2_duplicates": duplicates2,
        "common_elements": len(set(elements1) & set(elements2)),
        "file1_unique_elements": len(set(elements1) - set(elements2)),
        "file2_unique_elements": len(set(elements2) - set(elements1))
    }

    return results

def print_comparison_report(results):
    """
    Print a formatted comparison report.

    Args:
        results (dict): Results from compare_html_files
    """
    print("\nHTML Files Comparison Report")
    print("=" * 30)
    print(f"Similarity ratio: {results['similarity_ratio']:.2%}")

    if results['is_subset']:
        print(f"\nSubset detected: {results['subset_direction']}")

    print(f"\nCommon elements: {results['common_elements']}")
    print(f"Unique elements in file 1: {results['file1_unique_elements']}")
    print(f"Unique elements in file 2: {results['file2_unique_elements']}")

    if results['file1_duplicates']:
        print("\nDuplicates in file 1:")
        for elem, count in results['file1_duplicates'].items():
            print(f"  - Element repeated {count} times: {elem[:100]}...")

    if results['file2_duplicates']:
        print("\nDuplicates in file 2:")
        for elem, count in results['file2_duplicates'].items():
            print(f"  - Element repeated {count} times: {elem[:100]}...")

# Example usage
if __name__ == "__main__":
    # Example HTML content
    html1 = """
    <div>
        <p>Common content</p>
        <p>Common content</p>
        <span>Unique to file 1</span>
    </div>
    """

    html2 = """
    <div>
        <p>Common content</p>
        <p>Common content</p>
        <p>Common content</p>
    </div>
    """

    results = compare_html_files(html1, html2)
    print_comparison_report(results)