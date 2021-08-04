# -*- coding: utf-8 -*-

import re

import os
import shutil


class Static:

    namespace = set()


def def_namespace(path: str, newpath: str) -> bool:

    if path in Static.namespace:
        return False

    Static.namespace.add(newpath)

    return True


def def_depth(path: str, iformat: str = '.') -> int:

    nlevels = path.count(iformat)

    return nlevels - 1


def def_rdepth(dest: str, path: str, iformat: str = '/') -> int:

    nlevels = path.count(iformat)

    if path.startswith(dest):

        nlevels = path[len(dest):].count(iformat)

    return nlevels - 1


def path_join(dirpath: str, fname: str, fext: str):

    path = os.path.join(dirpath, fname) + fext

    return path


def realpath(path: str):

    rpath = os.path.realpath(path)

    return rpath


def sstrip(sstr: str, substr: str):

    l, r = 0, len(sstr)
    ls, rs = 1, 1

    while (r >= l) and (ls or rs):

        ls = int(sstr.startswith(substr, l, r))
        rs = int(sstr.endswith(substr, l, r))

        l += ls * len(substr)
        r -= rs * len(substr)

    return sstr[l:r]


def normalize_str(sstr: str):

    # sstr = re.sub(r'[^a-zA-Z0-9]', '', sstr)

    sstr = re.sub(r'\s+', '', sstr) 
    sstr = re.sub(r'[-|_]', '', sstr) 
    sstr = sstr.lower() 
    sstr = sstrip(sstr, '.')

    return sstr


def rclip(sstr: str, iformat: str, clipat: int):

    levels = sstr.split(iformat)

    if clipat >= len(levels):
        
        return sstr

    sstr = iformat.join(levels[-clipat:])

    return sstr


def find_ext(src: str, *ext):
    
    for (dirpath, _, filenames) in os.walk(src):
        
        for i in range(len(filenames)):

            fname, fext = os.path.splitext(filenames[i])

            for j in range(len(ext)):

                if fext == ext[j]:

                    yield dirpath, fname, fext


def ffind_ext(src: str, ext: str, src_include: bool = False, iformat: str = '.'):
    
    size = len(src)

    if src_include:

        size = 0

    for pargs in find_ext(src, ext):

        path = path_join(*pargs)
        
        newpath = path[size:].replace('/', iformat)
        newpath = normalize_str(newpath)

        yield path, newpath


def is_valid_path(src: str, dest: str):

    if not os.path.exists(src):

        print(f'dest: {src}, doesn\'t exist')

        return

    if not os.path.exists(dest):

        print(f'src: {src}, doesn\'t exist')

        return

    return 1


def fcopy_ext(src: str, dest: str, ext: str, src_include: bool = False, iformat: str = '.', clipat: int = 5):
    
    src = realpath(src)
    dest = realpath(dest)
    
    if not is_valid_path(src, dest):

        return

    pgen = ffind_ext(src, ext, src_include, iformat)

    for path, newpath in pgen:

        if not def_rdepth(dest, path):
            continue

        newpath = rclip(newpath, iformat, clipat)
        newpath = os.path.join(dest, newpath)

        if path == newpath:
            continue

        if not def_namespace(path, newpath):
            continue

        shutil.copyfile(path, newpath)
        
        print(newpath)


def fmove_ext(src: str, dest: str, ext: str, src_include: bool = False, iformat: str = '.', clipat: int = 5):

    src = realpath(src)
    dest = realpath(dest)

    if not is_valid_path(src, dest):

        return

    pgen = ffind_ext(src, ext, src_include, iformat)

    for path, newpath in pgen:

        if not def_rdepth(dest, path):
            continue

        newpath = rclip(newpath, iformat, clipat)
        newpath = os.path.join(dest, newpath)

        if not def_namespace(path, newpath):
            continue

        os.rename(path, newpath)

        print(newpath)


def args_info(func):

    count = func.__code__.co_argcount
    name = func.__code__.co_varnames
    defaults = func.__defaults__
    types = func.__annotations__

    return count, name, defaults, types


def unsafe_call(func):

    count, name, defaults, types = args_info(func)

    ecount = count - len(defaults)

    args = []

    for i in range(count):

        value = input(name[i] + ': ')
        
        if not len(value) and i >= ecount:

            args.append(defaults[i - ecount])

        else:

            value = types[name[i]](value)
            
            args.append(value)

    func(*args)


def run_cmd(cmd):

    print('\n' + realpath('./') + '\n')

    if cmd == 'mv':

        unsafe_call(fmove_ext)

    elif cmd == 'cp':

        unsafe_call(fcopy_ext)

    else:

        print('Command not found')
