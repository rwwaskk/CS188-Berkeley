# autograder.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# imports from python standard library
import grading
import imp
import optparse
import os
import re
import sys
import projectParams

# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(description = 'Run public tests on student code')
    parser.set_defaults(generateSolutions=False, edxOutput=False, muteOutput=False)
    parser.add_option('--test_directory',
                      dest = 'testRoot',
                      default = 'test_cases',
                      help = 'Root test directory which contains subdirectories corresponding to each question')
    parser.add_option('--student_code',
                      dest = 'studentCode',
                      default = projectParams.STUDENT_CODE_DEFAULT,
                      help = 'comma separated list of student code files')
    parser.add_option('--code_directory',
                    dest = 'codeRoot',
                    default = "",
                    help = 'Root directory containing the student and testClass code')
    parser.add_option('--test_case_code',
                      dest = 'testCaseCode',
                      default = projectParams.PROJECT_TEST_CLASSES,
                      help = 'class containing testClass classes for this project')
    parser.add_option('--generate-solutions',
                      dest = 'generateSolutions',
                      action = 'store_true',
                      help = 'Write solutions generated to .solution file')
    parser.add_option('--edx-output',
                    dest = 'edxOutput',
                    action = 'store_true',
                    help = 'Generate edX output files')
    parser.add_option('--mute',
                    dest = 'muteOutput',
                    action = 'store_true',
                    help = 'Mute output from executing tests')
    (options, args) = parser.parse_args(argv)
    return options

# confirm we should author solution files
def confirmGenerate():
    print 'WARNING: this action will overwrite any solution files.'
    print 'Are you sure you want to proceed? (yes/no)'
    while True:
        ans = sys.stdin.readline().strip()
        if ans == 'yes':
            break
        elif ans == 'no':
            sys.exit(0)
        else:
            print 'please answer either "yes" or "no"'

# create python modules from string representations of student code
def loadModuleDict(moduleCodeDict):
    moduleDict = {}
    for k in moduleCodeDict:
        # TODO: use the inbuilt compile() instead of exec?
        # This may help with naming the code correctly in exceptions
        # (currently we get the uninformative filename 'string')
        tmp = imp.new_module(k)
        exec moduleCodeDict[k] in tmp.__dict__
        moduleDict[k] = tmp
    return moduleDict

# read file from disk at specified path and return as string
def readFile(path, root=""):
    handle = open(os.path.join(root, path), 'r')
    text = handle.read()
    handle.close()
    return text


#######################################################################
# Error Hint Map
#######################################################################

# TODO: use these
ERROR_HINT_MAP = {
  'q1': {
    "<type 'exceptions.IndexError'>": """
      We noticed that your project threw an IndexError on q1.
      While many things may cause this, it may have been from
      assuming a certain number of successors from a state space
      or assuming a certain number of actions available from a given
      state. Try making your code more general (no hardcoded indices)
      and submit again!
    """
  },
  'q3': {
      "<type 'exceptions.AttributeError'>": """
        We noticed that your project threw an AttributeError on q3.
        While many things may cause this, it may have been from assuming
        a certain size or structure to the state space. For example, if you have
        a line of code assuming that the state is (x, y) and we run your code
        on a state space with (x, y, z), this error could be thrown. Try
        making your code more general and submit again!

    """
  }
}

# evaluate student code
def evaluate(generateSolutions, testRoot, moduleDict, exceptionMap=ERROR_HINT_MAP, edxOutput=False, muteOutput=False):
    # imports of testbench code.  note that the testClasses import must follow
    # the import of student code due to dependencies
    import testParser
    import testClasses
    for module in moduleDict:
        setattr(sys.modules[__name__], module, moduleDict[module])

    # iterate through and run tests
    test_subdirs = os.listdir(testRoot)
    questions = []
    for i in test_subdirs:
        subdir_path = os.path.join(testRoot, i)
        if not os.path.isdir(subdir_path) or i[0] == '.':
            continue

        # create a question object
        questionDict = testParser.TestParser(os.path.join(subdir_path, 'CONFIG')).parse()
        questionClass = getattr(testClasses, questionDict['class'])
        question = questionClass(questionDict)

        # load test cases into question
        tests = filter(lambda t: re.match('[^#~]*\.test\Z', t), os.listdir(subdir_path))
        tests = map(lambda t: re.match('(.*)\.test\Z', t).group(1), tests)
        for t in tests:
            test_file = os.path.join(subdir_path, '%s.test' % t)
            solution_file = os.path.join(subdir_path, '%s.solution' % t)
            testDict = testParser.TestParser(test_file).parse()
            if testDict.get("disabled", "false").lower() == "true":
                continue
            testClass = getattr(projectTestClasses, testDict['class'])
            testCase = testClass(testDict)
            def makefun(testCase, solution_file):
                if generateSolutions:
                    # write solution file to disk
                    return lambda grades: testCase.writeSolution(moduleDict, solution_file)
                else:
                    # read in solution dictionary and pass as an argument
                    solutionDict = testParser.TestParser(solution_file).parse()
                    return lambda grades: testCase.execute(grades, moduleDict, solutionDict)
            question.addTestCase(testCase, makefun(testCase, solution_file))

        # Note extra function is necessary for scoping reasons
        def makefun(question):
            return lambda grades: question.execute(grades)
        setattr(sys.modules[__name__], i, makefun(question))
        questions.append((i, question.getMaxPoints()))

    grades = grading.Grades(projectParams.PROJECT_NAME, questions, edxOutput=edxOutput, muteOutput=muteOutput)
    grades.grade(sys.modules[__name__])    
    return grades.points



if __name__ == '__main__':
    options = readCommand(sys.argv)
    if options.generateSolutions:
        confirmGenerate()
    moduleCodeDict = {}
    codePaths = options.studentCode.split(',')
    for cp in codePaths:
        moduleName = re.match('.*?([^/]*)\.py', cp).group(1)
        moduleCodeDict[moduleName] = readFile(cp, root=options.codeRoot)
    moduleCodeDict['projectTestClasses'] = readFile(options.testCaseCode, root=options.codeRoot)
    moduleDict = loadModuleDict(moduleCodeDict)
    evaluate(options.generateSolutions, options.testRoot, moduleDict, edxOutput=options.edxOutput, muteOutput=options.muteOutput)
