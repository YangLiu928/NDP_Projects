codes = ['01','0101','0102','02','0201','020101','0202','020201','020202']


def get_relationship(codes):
    stack = ['0']
    result = {'0':[]}
    for code in codes:
        current_parent = stack[len(stack)-1] # basically a peek method
        if len(code)==len(current_parent):
            # this means that, the line of "code" being examined now is at the same level of the previous line
            # also, this means that, the current_parent does not have any children, because the initial input is sorted
            stack.pop()
            # since, each time a code without children got popped, the next member in the stack is surely the real parent
            # level of the current entry (code in this case)
            real_parent = stack[len(stack)-1]
            # insert the relationship into the result dictionary

            # need to push the current entry into the stack, in case the next line of codes is its children
        elif len(code) > len(current_parent):
            real_parent = current_parent
        else:
            while (len(stack[len(stack)-1])>=len(code)):
                stack.pop()
            real_parent = stack[len(stack)-1]

        if result.has_key(real_parent):
            result[real_parent].append(code)
        else:
            result[real_parent] = [code]

        stack.append(code)
    return result


if __name__ == '__main__':
    print get_relationship(codes)
