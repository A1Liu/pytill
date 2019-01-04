# -*- coding: utf-8 -*-
import shutil
# Simple statement of memory usage
def memory_statement(savings,task_name,statement):
    return  statement \
              .format( convert_memory(savings) ,task_name )

# Convert memeory to a readable form
def convert_memory(memory_value):
    unit_list = ['KB','MB','GB','TB']
    index = 0
    memory = memory_value / 1024
    while memory > 1000 and index < 3:
        memory/=1024
        index+=1
    return '{} {}'.format(round( memory, 1),unit_list[index])

def title_line(text):
    """Returns a string that represents the
    text as a title blurb
    """
    columns = shutil.get_terminal_size()[0]
    start = columns // 2 - len(text) // 2
    output = '='*columns + '\n\n' + \
            ' ' * start + str(text) + "\n\n" + \
            '='*columns + '\n'
    return output

# Outputs to a file. If and only if ouput_safe is false, it will overwrite existing files
def output_to_file(df,output_file,output_safe):
    try:
        with open(output_file,'x' if output_safe else 'w') as file:
                file.write(df)
    except FileExistsError:
        print("Nothing outputted: file '{}' already exists".format(output_file))