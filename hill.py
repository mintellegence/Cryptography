import numpy as np
from sympy import Matrix
from sympy.matrices.common import NonInvertibleMatrixError

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.OKGREEN}{bcolors.BOLD}\n***** Author: SHARIF HUSSAIN 11720 *****{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}{bcolors.BOLD}******** Cryptography & DataSEC *********{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}{bcolors.BOLD}****************************************{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}{bcolors.BOLD}\nHill's Cypher\n{bcolors.ENDC}")

# Global Variables
KEY = ''
N = 0
ENCRYPT = 'PLAINTEXT'
DECRYPT = 'CYPHERTEXT'
KEY_LIST = []

# Convert Function
def convert(s):
        str = ''
        for x in s:
            str += x
        return str

def mod_func_list(lst):
        ind = 0
        for x in lst:
            if x >= 97 and x <= 122:
                    lst[ind] -= 97    
            elif x >= 65 and x <= 90:
                    lst[ind] -= 65 
            ind += 1
        return lst

def mod_func_matrix(lst,mat):
        ind = 0
        for x in lst:
            if x >= 97 and x <= 122:
                    mat[ind] += 97    
            elif x >= 65 and x <= 90:
                    mat[ind] += 65 
            ind += 1
        return mat

def ignore_space(space):

    space_list = [x for x in space]

    indices = []
    for i in range(0, len(space_list)):
        if space_list[i] == ' ':
            indices.append(i) 

    for x in sorted(indices, reverse=True):
        del space_list[x]

    return space_list, indices

def to_list_matrix(msg, key, n):
    
    text_list = [ord(x) for x in msg]
    ref_text = [ord(x) for x in msg]
    K_LIST = [ord(x) for x in key]

    text_list_mod = mod_func_list(text_list)
    KEY_LIST = mod_func_list(K_LIST)

    # Message Matrix
    msg_matrix = np.array(list(text_list_mod))[np.newaxis]
    msg_matrix_t = msg_matrix.T

    #Key Matrix
    key_matrix = np.array(list(KEY_LIST)).reshape(n,n)
    key_matrix = key_matrix % 26

    return key_matrix, msg_matrix_t, ref_text

def proc_matrix_inverse(matrix):
     # *** KEY Matrix Inverse Function ***
    try:
         # Using SYMPY.MATRIX library for Inverse
        mat_inv = Matrix(matrix)
        inverted_mat = mat_inv.inv_mod(26)
    
    except NonInvertibleMatrixError :
        print(f"{bcolors.FAIL}\n!!! Key Matrix non Invertible !!!\n{bcolors.ENDC}")
        return 0
    
    return inverted_mat

# Input Function
def inp(encdec):
    # Prints plainText / CypherText
    print('Input ' + encdec + ': ')
    
    # Takes input
    raw = input("")
    print('\nPLAINTEXT: ' + raw)

    # Function for ignoring spaces
    msg, indices = ignore_space(raw)

    N = len(msg)
    total = N*N
    print('\nInput key of exactly ', total, ' Characters:')
    
    def key_input(total):

        key = input('')

        if len(key) < total:
            while (len(key) != total):
                print(f"{bcolors.FAIL}\n!!! Read the Instructions Carefully !!!\n{bcolors.ENDC}")
                print('Enter key of exactly ', total, ' charcters: ')
                key = input('')

        print(f"{bcolors.OKBLUE}\n!!! Key Accepted !!!\n{bcolors.ENDC}")
        print('KEY: ', key)
        
        return key

    KEY = key_input(total)

    return N,KEY, indices, msg


# Encrypt Function
def encrypt():
    
    N, KEY, indices, message = inp(ENCRYPT)    

    # Convering to Numpy Matrix & Printing
    key_matrix, p_matrix, ref_text = to_list_matrix(message, KEY, N)
    print('\nPlainText Matrix: \n', p_matrix)
    print('\nKey Matrix: \n', key_matrix)
    
    # Inverse of KEY MAtrix
    result_mat = proc_matrix_inverse(key_matrix)
        
    if result_mat == 0:
        return 0

    # Multiplying Key Matrix with Plain text Matrix
    c_matrix = np.matmul(key_matrix, p_matrix)
    
    # Applying MOD 26
    c_matrix = c_matrix % 26
    c_matrix = mod_func_matrix(ref_text, c_matrix)

    print('\nMatrx Multiplication Result: \n', c_matrix)
    
    # Converts ASCII to chr
    c_list = [chr(x) for x in c_matrix]
    
    # Inserting back spaces if any
    for y in indices:
        c_list.insert(y, ' ')
    
    # Convering to String(text)
    cypherText = convert(c_list)

    print(f"{bcolors.OKGREEN}{bcolors.BOLD}\nCypherText: {cypherText}{bcolors.ENDC}")
    print('\n')
    return 

    # Decrypt Function
def decrypt():
        
        N, KEY, indices, message = inp(DECRYPT)
        
        # Convering to Numpy Matrix & Printing
        key_matrix, c_matrix, ref_text = to_list_matrix(message, KEY, N)
        print('\nCypherText Matrix: \n', c_matrix)
        print('\nKey Matrix: \n', key_matrix)
        
        # Inverse of KEY MAtrix
        result_mat = proc_matrix_inverse(key_matrix)
        
        if result_mat == 0:
            return 0

        # Again Converting to np.array from sympy matrix
        key_mat_inv = np.array(result_mat, dtype=np.int32)
        
        # Applying MOD 26
        key_mat_inv = key_mat_inv % 26
        print('\nKey Matrix Inverse: \n', key_mat_inv)

        # Multiplying Key Matrix Inverse with CypherText
        c_matrix = np.matmul(key_mat_inv, c_matrix)
        
        # Applying MOD 26 
        c_matrix = c_matrix % 26
        c_matrix = mod_func_matrix(ref_text, c_matrix)
        print('\nMatrx Multiplication Result: \n', c_matrix)
        
        # Convering int to chr
        p_matrix = [chr(x) for x in c_matrix]

        # Inserting back spaces if any
        for y in indices:
            p_matrix.insert(y, ' ')

        # converting list into String(Text)
        plainText = convert(p_matrix)

        print(f"{bcolors.OKGREEN}{bcolors.BOLD}\nPlainText: {plainText}{bcolors.ENDC}")
        print('\n')
        
        return

# MENU
def menu():
    def print_menu():
        print('Enter your choice: ')
        print("=>  Enter 1 for 'Encryption'")
        print("=>  Enter 2 for 'Decryption'")
        print("=>  Enter 0 to 'Exit'")

    count = True 
    
    while count:
        print_menu()
        inp = input('')

        if inp == '1':
            print(f"{bcolors.OKGREEN}{bcolors.BOLD}\n******Encryption*******\n{bcolors.ENDC}")
            encrypt()
        
        elif inp == '2':
            print(f"{bcolors.OKGREEN}{bcolors.BOLD}\n******Decryption*******\n{bcolors.ENDC}")
            decrypt()
        
        elif inp == '0':
            count = False
            break
        else:
            input("Invalid input, Press RETURN to try again!")
    
    return

menu()
