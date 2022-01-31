import numpy as np

# Returns the technicians, as a dict object.
# Key is the technician's name, value is their
# annual salary. The dict object is built up from lines in the
# CSV file whose name is passed as a parameter:
def read_technicians(file_name):
    file = open(file_name, 'r')

    technicians = {}

    for line in file:
        line_elements = line.split(',')
        technicians[line_elements[0]] = float(line_elements[1])

    return technicians

# Returns the MRI procedures, as a dict object.
# Key is the integer code for the procedure, value is
# procedure name or description. The dict object is built up
# from lines in the file whose name is passed as a parameter and
# where the code and name are separated by the "|" character:s
def read_mri_procs(file_name):
    file = open(file_name, 'r')

    mri_procs = {}

    for line in file:
        line_elements = line.split('|')
        mri_procs[int(line_elements[0])] = line_elements[1]

    return mri_procs

# Prints out the selection of MRI exams for the
# user to choose from, and then returns the procedure
# code for the procedure chosen by the user, validating
# that it is indeed a valid code:
def get_mri_proc_option_from_user(mri_procs):
    proc_code = -1
    while proc_code == -1:
        print('\nThe follow exams are available:\n')
        for pc in mri_procs.keys():
            print('{} ({})'.format(mri_procs[pc], pc))

        proc_code = int(input('\nPlease select your exam by entering the numeric procedure code: '))
        if proc_code not in mri_procs.keys():
            print('\nSorry, that was an invalid procedure code. Please try again...\n')
            proc_code = -1

    return proc_code

# Prints out the selection of available MRI technicians for
# the user to choose from, then returns the technician's
# name as a string, validating that the name is valid:
def get_technician_from_user(mri_techs):
    technician_index = -1
    technician_names = list(mri_techs.keys())
    while technician_index == -1:
        print('\nChoose from the following MRI technicians:\n')
        for i in range(len(technician_names)):
            print('{}.) {}'.format(i + 1, technician_names[i]))

        technician_index = int(input('\nPlease choose your option [1 to {}]: '.format(len(technician_names))))
        if technician_index < 1 or technician_index > len(technician_names):
            print('\nSorry, that was an invalid procedure code. Please try again...\n')
            technician_index = -1

    return technician_names[technician_index-1]

# Main function that estimates the true cost of MRI exam
def mri_exam_estimate(mri_proc_data, mri_technicians, final_proc_code, technicians):
    mri_data = mri_proc_data[mri_proc_data[:, 0] == final_proc_code]
    base_proc_cost = mri_data[0, 1]
    min_average_proc = sum(mri_data[0, 2:]) / len(mri_data[0, 2:])
    tech_salaries = mri_technicians[technicians]

    return base_proc_cost + ((tech_salaries * min_average_proc) / (52 * 40 * 60))

# Grabs the CSV files from the pre-generated MRI data folder, establishes delimiter
mri_proc_data = np.genfromtxt('data\\mri-proc-data.csv', delimiter=',')
technicians = read_technicians('data\\technician-salaries.csv')
mri_procedures = read_mri_procs('data\\mri-procedures.csv')

# Allows user to perform multiple calculations with a "yes" or "y" response,
# Returns results from variables above and inserts them into a string with
# correct numerical formatting. 
go_again = 'y'
while go_again == 'y' or go_again == 'yes':
    current_proc_code = get_mri_proc_option_from_user(mri_procedures)
    current_technician = get_technician_from_user(technicians)
        

    calc_proc_cost = mri_exam_estimate(mri_proc_data, technicians, current_proc_code, current_technician)

    print('\nThe estimated cost of the {} (code:{}) procedure, performed by {}, is ${:,.2f}'.format(mri_procedures[current_proc_code], current_proc_code, current_technician, calc_proc_cost))

    go_again = input('\nWould you like to go again? y/n: ').strip().lower()

print('\nThanks for using the MRI cost calculator, goodbye!')
