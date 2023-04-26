
# @Author : fly1ngpengu1ns
import re

# 需要删掉的规则, 可以自己加规则
rules = [b'The scope of the variable', b'is never used', b'can be declared with const',
         b'Skipping configuration', b'Cppcheck failed to extract a valid configuration',
         b'Cppcheck cannot find all the include files', b'Redundant assignment',
         b'No header in #include', b'There is an unknown macro here somewhere',
         b'syntax error', b'Too many #ifdef configurations', b'failed to expand',
         b'Unused variable:', b"is of type 'void *'. When using void pointers",
         b'There is #if in function body', b'C-style pointer casting',
         b'Comparing pointers that point to different objects',
         b'Uninitialized struct member', b'invalidPrintfArgType',
         b'Wrong number of parameters for macro', b"Identical inner 'if' condition"]

# 输入仓库定位至具体代码的url前缀
# 请注意, 确保cppcheck所检查的代码是最新版本, 否则将导致url定位失败！
url_prefix = b'https://github.com/OpenAtomFoundation/TencentOS-tiny/tree/master'
# 输入扫描的、已下载文件夹的名称
# 请注意, 该文件夹应该是git clone后直接解压缩得到的文件夹, 而不是仓库中的某一个文件夹
dir_name = b'TencentOS-tiny-master'


def get_url(txt: bytes):
    # 通过匹配文件夹前缀和代码行数, 确定文件url并返回
    start = txt.find(dir_name) + len(dir_name)
    end = re.search(b'[0-9]+:', txt).span()
    url = url_prefix + txt[start:end[0]-1] + b'#L' + txt[end[0]:end[1]] + b'\n'
    return url


def write_three_lines(dst, src, txt: bytes):
    # 将待写入的信息txt以及src中接下来的两行内容写入dst中, 并返回下一个待检测的信息txt
    dst.write(txt)
    dst.write(src.readline())
    dst.write(src.readline())
    return src.readline()


with open('output-cppcheck.txt', 'rb') as f1:
    with open('newnew.txt', 'wb') as f2:
        with open('WarnAndErr.txt', 'wb') as f3:
            txt = f1.readline()
            while txt:
                flag = False
                for rule in rules:
                    if rule in txt:
                        f1.readline()
                        f1.readline()
                        txt = f1.readline()
                        flag = True
                        break
                if flag:
                    continue

                # 对于这个fp, 直接忽略所有信息
                if b'shadows outer variable' in txt:
                    f1.readline()
                    f1.readline()
                    txt = f1.readline()
                    while b'note:' in txt:
                        f1.readline()
                        f1.readline()
                        txt = f1.readline()

                # 对于这个错误, 有可能是函数根本没写, 错误内容将指向'}', 这种必定是fp
                if b'missingReturn' in txt:
                    txt1 = f1.readline()
                    if txt1[0:1] == b'}':
                        f1.readline()
                        txt = f1.readline()
                    else:
                        f3.write(get_url(txt))
                        f3.write(txt)
                        f3.write(txt1)
                        f3.write(f1.readline())
                        txt = f1.readline()

                        while b'note:' in txt:
                            txt = write_three_lines(f3, f1, txt)
                        f3.write(b'\n')
                    continue

                # 把warning、error和一个错误率高的问题丢到WarnAndErr.txt
                if b'warning:' in txt or b'error:' in txt or b'Same expression on both sides of' in txt:
                    f3.write(get_url(txt))
                    txt = write_three_lines(f3, f1, txt)

                    while b'note:' in txt:
                        txt = write_three_lines(f3, f1, txt)
                    f3.write(b'\n')
                else:
                    # 把除了需要收集的信息外, 不删的部分丢到newnew里面去
                    f2.write(get_url(txt))
                    txt = write_three_lines(f2, f1, txt)
                    while b'note:' in txt:
                        txt = write_three_lines(f2, f1, txt)
                    f2.write(b'\n')
