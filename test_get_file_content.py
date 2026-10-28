from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt truncated: {'truncated' in result}")

result = get_file_content("calculator", "main.py")
print(result[:200])

result = get_file_content("calculator", "pkg/calculator.py")
print(result[1500:1700])

print(get_file_content("calculator", "/bin/cat"))

print(get_file_content("calculator", "pkg/does_not_exist.py"))
