import os
import sys
import subprocess

class PlaygroundC():
    # Initializes the PlaygroundC class
    # Required Variables
    #           prog_file_name - user's token for unique file names 
    #           code           - in case you want to have something in the file while creation
    
    def __init__(self, prog_file_name, code=None):
    # Initializes itself with parameters:
    #        compiler  - gcc Compiler
    #        code_file - where the .c file is stored
    #        run_file  - where the compiled file is stored
    #        code      - String with the code
        self.compiler = 'gcc'
        self.code_file = './modelsTest/user_codes/C_Files/' + prog_file_name + '.c'
        self.run_file = './modelsTest/user_codes/Compiled_Files/' + prog_file_name
        self.code = code

    def compile_code(self):
    # Function to compile the code
        shell_command = [self.compiler, self.code_file, '-o', self.run_file] # '-Wall', 
        program = subprocess.Popen(shell_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            result = program.wait(timeout=10)
        except subprocess.TimeoutExpired:
            result = program.terminate()
        a, b = program.communicate()
        self.stdout, self.stderror = a.decode('utf-8'), b.decode('utf-8')
        return result

    def run_code(self):
    # Function to run the C code
        shell_command = self.run_file
        program = subprocess.Popen(shell_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = program.wait()
        a, b  = program.communicate()
        self.stdout, self.stderror = a.decode('utf-8'), b.decode('utf-8')
        return result

    def run_c_program(self):
    # This function calls compile_code and run_code to get the final outputs
    # Outputs:
    #   result_compilation - output from the compile_code function
    #   result_run         - output from the run_code function
        result_run = "The program might have errors !!"
        with open(self.code_file, 'w') as f:
            f.write("#include<stdio.h>\n")
            f.write(self.code)
            f.close()
        result = self.compile_code()
        # print("\n")
        # print("Printing Compiling result")
        # print(result)
        # print("\n")
        result_compilation = self.stdout + self.stderror
        if result == 0:
            self.run_code()
            result_run = self.stdout + self.stderror
        return result_compilation, result_run

        


