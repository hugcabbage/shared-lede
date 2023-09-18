# 简化.config，仅保留应用和主题
def simplify_config(file: str, *, backup=True, remain_text=None):
    inxheader = ()
    inxapp = ()
    inxtheme = ()
    header_flag = True
    with open(file) as f:
        text = f.readlines()
    if backup:
        with open(file + '.fullbak', 'w') as f:
            f.writelines(text)
    for (index, value) in enumerate(text):
        if value.startswith('CONFIG_TARGET') and '=y' in value and header_flag:
            inxheader += (index,)
            if len(inxheader) == 3:
                header_flag = False
        elif '. Applications' in value:
            inxapp += (index,)
        elif '. Themes' in value:
            inxtheme += (index,)
    header = ['# Target\n']
    for i in inxheader:
        header += [text[i]]
    apps = list(filter(lambda x: x.strip('#\n') and '# Configuration' not in x and '# end of' not in x, text[inxapp[0]:inxapp[1]]))
    apps = list(map(lambda x: '# Applications\n' if '. Applications' in x else x, apps))
    themes = list(filter(lambda x: x.strip('#\n') and '# end of' not in x, text[inxtheme[0]:inxtheme[1]]))
    themes = list(map(lambda x: '# Themes\n' if '. Themes' in x else x, themes))
    for part in header, apps:
        part.append('\n')
    if remain_text:
        remain_text.append('\n')
        text = header + remain_text + apps + themes
    else:
        text = header + apps + themes        
    with open(file, 'w') as f:
        f.writelines(text)
