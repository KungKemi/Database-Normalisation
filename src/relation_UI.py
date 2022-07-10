__author__ = "Alexander Johnson"
__email__ = "work.a.a.johnson@gmail.com"
__date__ = "27/06/2021"

from set_theory import Set
from relation import Rel


def extract_info(txt_file, info):
    """Method to extract information from text file

    Parameters:
        txt_file(list): the imported text file
        info(str): line in text file from which to start search
    """
    pos = txt_file.index(info + '\n')
    txt = []
    arg = txt_file[pos]
    while arg != '\n':
        pos += 1
        txt.append(txt_file[pos].strip('\n'))
        arg = txt_file[pos]
    return txt


def main():
    """Handles top-down interaction with relation.py"""
    f = open('assets/relation_UI.txt', 'r').readlines()
    relations = []
    panel = 'menu'
    option = ''
    # Extract relevant information from relation_UI.txt
    for line in extract_info(f, '[credits]'):
        print(line)
    query = extract_info(f, '[input]')
    error = extract_info(f, '[error]')
    attribute = extract_info(f, '[attribute]')
    menu = extract_info(f, '[menu]')
    creator = extract_info(f, '[creator]')
    select = extract_info(f, '[select]')
    relation = extract_info(f, '[relation]')
    delete = extract_info(f, '[delete]')
    depend = extract_info(f, '[depend]')
    compute = extract_info(f, '[compute]')
    decomp = extract_info(f, '[decomp]')
    while option != 'q':
        # menu interface
        if panel == 'menu':
            for line in menu:
                print(line)
            while panel == 'menu':
                print(73 * '-')
                option = input(query[0]).strip()
                while option not in ['1', '2', 'q']:
                    print(error[0])
                    option = input(query[0]).strip()
                if option == '1':
                    panel = 'creator'
                elif option == '2':
                    panel = 'select'
                else:
                    break
        # interface to create relation 
        if panel == 'creator':
            print(73 * '-')
            num_rel = len(relations)
            print(creator[0].format(num_rel), '\n')
            if num_rel == 3:
                print(creator[1])
                panel = 'delete'
            # prompt user to create relation
            else:
                print(attribute[0], '\n')
                attr_list = input(attribute[1]).split(',')
                new_rel = []
                for attr in attr_list:
                    attr.strip()
                    new_rel.extend(attr.split())
                relations.append(Rel(*new_rel))
                panel = 'menu'
        # interface to select relation 
        if panel == 'select':
            num_rel = len(relations)
            # if no relation is defined, go to menu or creator
            if num_rel == 0:
                print(73 * '-')
                option = input(select[5]).strip()
                while option.capitalize() not in ['Y', 'N']:
                    print(error[0])
                    option = input(select[5]).strip()
                if option.capitalize() == 'Y':
                    panel = 'creator'
                else:
                    panel = 'menu'
            # prompt user to select defined relation(s)
            else:
                for line in select[:num_rel + 1]:
                    print(line)
                print(select[4], '\n')
                print(73 * '-')
                option = input(query[0]).strip()
                options = ['m']
                for choice in range(1, num_rel + 1):
                    options.append(str(choice))
                while option not in options:
                    print(error[0])
                    option = input(query[0]).strip()
                if option == 'm':
                    panel = 'menu'
                else:
                    select_rel = relations[num_rel - 1]
                    panel = 'relation'
        # interface to interact with select_rel 
        if panel == 'relation':
            for line in relation[:7]:
                print(line)
            print()
            while panel == 'relation':
                print(73 * '-')
                option = input(query[0]).strip()
                while option not in ['1', '2', '3', '4', 'r', 'm']:
                    print(error[0])
                    option = input(query[0]).strip()
                if option == '1':
                    panel = 'depend'
                elif option == '2':
                    panel = 'compute'
                elif option == '3':
                    print(select_rel)
                    if len(select_rel.FD_LHS()) == 0:
                        print('No dependencies currently defined')
                # prompt user to delete selected relation
                elif option == '4':
                    option = input(relation[7]).strip()
                    while option.capitalize() not in ['Y', 'N']:
                        print(error[0])
                        option = input(relation[7]).strip()
                    if option.capitalize() == 'Y':
                        relations.remove(select_rel)
                        panel = 'menu'
                elif option == 'r':
                    panel = 'select'
                else:
                    panel = 'menu'
        # interface to delete relation 
        if panel == 'delete':
            for line in delete:
                print(line)
            print(73 * '-')
            option = input(query[0]).strip()
            while option not in ['1', '2', '3', 'm']:
                print(error[0])
                option = input(query[0]).strip()
            if option in ['1', '2', '3']:
                relations.pop(int(option) - 1)
                panel = 'creator'
            else:
                panel = 'menu'
            print()
        # interface to add/remove dependencies for select_rel 
        if panel == 'depend':
            for line in depend[:6]:
                print(line)
            print()
            while panel == 'depend':
                print(73 * '-')
                option = input(query[0]).strip()
                while option not in ['1', '2', '3', 'r', 'm']:
                    print(error[0])
                    option = input(query[0]).strip()
                # add a dependency
                if option == '1':
                    # ask user how many FDs they would like to add
                    num_FDs = input(depend[6]).strip()
                    while not num_FDs.isdigit() or not int(num_FDs) > 0:
                        print(error[1])
                        num_FDs = input(depend[6]).strip()
                    print(attribute[0], '\n')
                    # for each FD, request input for LHS and RHS
                    # input must include attributes from relation, and
                    # FD must be non-trivial
                    for index in range(1, int(num_FDs) + 1):
                        print(depend[7].format(index))
                        FD_list = []
                        for j in range(2):
                            while True:
                                FD_side = []
                                attr_list = input(depend[8 + j]).split(',')
                                for attr in attr_list:
                                    attr.strip()
                                    FD_side.extend(attr.split())
                                FD_side = Set(*FD_side)
                                if not FD_side.subset(select_rel.attributes()):
                                    print(error[2])
                                elif j == 1 and FD_side - FD_list[0] != FD_side:
                                    print(error[3])
                                else:
                                    FD_list.append(FD_side)
                                    break
                        FD_LHS = FD_list[0].elements()
                        FD_RHS = FD_list[1].elements()
                        select_rel.add_FD(FD_LHS, FD_RHS)
                        print()
                # select which FD to remove
                elif option == '2':
                    if len(select_rel.FD_LHS()) == 0:
                        print(error[4])
                    else:
                        FD = input(depend[10]).strip()
                        num_FDs = len(select_rel.FD_LHS())
                        while True:
                            if not FD.isdigit() or not int(FD) > 0:
                                print(error[1])
                            elif int(FD) > num_FDs:
                                print(error[5].format(num_FDs))
                            else:
                                break
                            FD = input(depend[10]).strip()
                        select_rel.remove_FD(int(FD))
                # prompt user to delete all dependencies
                elif option == '3':
                    option = input(depend[11]).strip()
                    while option.capitalize() not in ['Y', 'N']:
                        print(error[0])
                        option = input(depend[11]).strip()
                    if option.capitalize() == 'Y':
                        select_rel.reset_FD()
                        panel = 'menu'
                # go to previous panel
                elif option == 'r':
                    panel = 'relation'
                else:
                    panel = 'menu'
        # interface to compute results for select_rel 
        if panel == 'compute':
            for line in compute[:8]:
                print(line)
            print()
            while panel == 'compute':
                print(73 * '-')
                option = input(query[0]).strip()
                while option not in ['1', '2', '3', '4', '5', 'r', 'm']:
                    print(error[0])
                    option = input(query[0]).strip()
                # compute closure, where attributes must be in relation
                if option == '1':
                    print(attribute[0], '\n')
                    while True:
                        attr_list = input(attribute[1]).split(',')
                        close = []
                        for attr in attr_list:
                            attr.strip()
                            close.extend(attr.split())
                        close_set = Set(*close)
                        if not close_set.subset(select_rel.attributes()):
                            print(error[2])
                        else:
                            break
                    print(compute[8], select_rel.closure(close_set).elements())
                # compute candidate keys for relation
                elif option == '2':
                    K = select_rel.keys()
                    print(compute[9].format(K.card()), '\n')
                    for i, key in enumerate(K.elements(), 1):
                        print(str(i) + '.', key.elements())
                # super key test, where attributes must be in relation
                elif option == '3':
                    print(attribute[0], '\n')
                    while True:
                        attr_list = input(attribute[1]).split(',')
                        supkey = []
                        for attr in attr_list:
                            attr.strip()
                            supkey.extend(attr.split())
                        supkey_set = Set(*supkey)
                        if not supkey_set.subset(select_rel.attributes()):
                            print(error[2])
                        else:
                            break
                    print(compute[10], select_rel.super_key(supkey_set))
                # compute highest normal form
                elif option == '4':
                    HNF = select_rel.highest_NF()
                    print(compute[11].format(HNF), '\n')
                    if HNF != 'BCNF':
                        NFs = ['1NF', '2NF', '3NF', 'BCNF']
                        viol = NFs[NFs.index(HNF) + 1]
                        # if HNF is not BCNF, prompt user if they would
                        # like to know first instance of violation
                        option = input(compute[12].format(viol)).strip()
                        while option.capitalize() not in ['Y', 'N']:
                            print(error[0])
                            option = input(compute[12].format(viol)).strip()
                        if option.capitalize() == 'Y':
                            print()
                            if viol == '2NF':
                                select_rel.two_NF_reason()
                            elif viol == '3NF':
                                select_rel.three_NF_reason()
                            else:
                                select_rel.BCNF_reason()
                elif option == '5':
                    panel = 'decomp'
                elif option == 'r':
                    panel = 'relation'
                else:
                    panel = 'menu'
        # interface to normalise select_rel
        if panel == 'decomp':
            for line in decomp[:6]:
                print(line)
            print()
            while panel == 'decomp':
                print(73 * '-')
                option = input(query[0]).strip()
                while option not in ['1', '2', '3', 'r', 'm']:
                    print(error[0])
                    option = input(query[0]).strip()
                # compute minimal cover, prompt for union
                if option == '1':
                    option = input(decomp[6]).strip()
                    while option.capitalize() not in ['Y', 'N']:
                        print(error[0])
                        option = input(decomp[6]).strip()
                    print()
                    if option.capitalize() == 'Y':
                        print(select_rel.min_cover(True))
                    else:
                        print(select_rel.min_cover())
                # perform 3NF decomposition if HNF < 3NF
                elif option == '2':
                    print(select_rel.three_NF_decomp())
                # perform BCNF decomposition if HNF < BCNF
                elif option == '3':
                    print(select_rel.BCNF_decomp())
                elif option == 'r':
                    panel = 'compute'
                else:
                    panel = 'menu'


if __name__ == "__main__":
    main()
