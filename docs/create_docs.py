import inspect
import rubrik
import os


def print_doc_string(doc_string):
    for line in doc_string:
        markdown.write(line.strip() + '\n\n')


rubrk_sdk_functions = inspect.getmembers(rubrik.Connect, inspect.isfunction)

function_examples = {}
function_documentation = {}
for function in rubrk_sdk_functions:
    function_documentation[function[0]] = function[1].__doc__
    function_code = inspect.getsource(function[1])
    if '@staticmethod' in function_code:
        function_code = function_code.splitlines()[1].replace(
            'self, ', '').replace('self', '').replace(':', '').strip()
    else:
        function_code = function_code.splitlines()[0].replace(
            'self, ', '').replace('self', '').replace(':', '').strip()

    function_examples[function[0]] = function_code


for function_name, function_doc_string in function_documentation.items():
    if 'init' not in function_name:
        markdown = open('{}.md'.format(function_name), 'w')
        markdown.write('# {}\n\n'.format(function_name))

        doc_string = function_documentation[function_name]
        doc_string = doc_string.splitlines()

        filter_lines = []

        for index, line in enumerate(doc_string):
            if 'Arguments' in line:
                filter_lines.append(index)
            if 'Returns' in line:
                filter_lines.append(index)

            # print(index, line)

        arguments = []
        keyword_arguments = []
        returns = []
        desctiption = []

        try:
            arguments_start = filter_lines[0]
            keyword_arguments_start = filter_lines[1]
            returns_start = filter_lines[2]
        except:
            pass
        # Doc Sring Returns
        for index, line in enumerate(doc_string):
            # Parse the function description
            if len(filter_lines) >= 0:
                if index < arguments_start:
                    if len(line) is not 0:
                        desctiption.append(line)

            # Parse the function arguments
            if len(filter_lines) > 1:
                if arguments_start + 1 <= index <= keyword_arguments_start - 1:
                    if len(line) is not 0:
                        arguments.append(line)

            # Parse the function keyword arguments
            if len(filter_lines) >= 2:
                if keyword_arguments_start + 1 <= index <= returns_start - 1:
                    if len(line) is not 0:
                        keyword_arguments.append(line)

            # Parse the function return value(s)
            if len(filter_lines) >= 3:
                if index >= returns_start + 1:
                    if len(line) is not 0:
                        returns.append(line)

        # print(index, line)
        if desctiption:
            print_doc_string(desctiption)

        for function, function_code_example in function_examples.items():
            if function_name is function:
                markdown.write('```py\n')
                markdown.write(function_code_example)
                markdown.write('\n```\n\n')

        if arguments:
            markdown.write('## Arguments\n')
            print_doc_string(arguments)

        if keyword_arguments:
            markdown.write('\n## Keyword Arguments\n')
            print_doc_string(keyword_arguments)

        if returns:
            markdown.write('\n## Returns\n')
            print_doc_string(returns)
