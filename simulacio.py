import random
import os
import os.path
import sys
import shutil

PORCENTAJE_INFECCION = 50
PORCENTAJE_RANSOM = 20
file_list_chunga = []
file_list_ransom = []
file_list_ok = []


def  create_config():
    config = {}

    config['dir_init'] = sys.argv[1]
    config['infeccion'] = []


    posibles_infecciones = ['size', 'content', 'extension', 'auth']

    val = random.randint(0, 100)
    print('Random para RANSOM',val)

    if val < PORCENTAJE_RANSOM:
        config['infeccion'].append('ransom')
        return config


    val = random.randint(0,100)

    # extensiones
    print('Random para INFECCION',val)
    if val < PORCENTAJE_INFECCION:
        for posible_infeccion in posibles_infecciones:
            val = random.randint(0, 100)
            if val < PORCENTAJE_INFECCION:
                config['infeccion'].append(posible_infeccion)

    return config




def generate_file(filename, size, config):

    infection_list=[]
    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


    # ARCHIVO RANSOM: caracteres aleatorios
    #if len(config['infeccion'])>0 and 'ransom' == config['infeccion'][0]:
    if  'ransom' in config['infeccion']:
        chars = ''.join([random.choice(['Z','Y','W']) for i in range(size)])
        with open(filename, 'w') as f:
            f.write(chars)
        file_list_ransom.append(filename)
        return


    # Se contruye simpre un ARCHIVO SANO:  caracteres ACGT
    num_lineas  = random.randint(1,5)
    lines = [str(num_lineas) + '\n']
    for i in range(num_lineas):
        line = ''
        line = ''.join([random.choice(['A','C','G','T']) for i in range(int(size / num_lineas))])  # 1
        line +='\n'
        lines.append(line)

    if 'size' in config['infeccion']:
        infected_lines_number = num_lineas
        while infected_lines_number == num_lineas:
            infected_lines_number = random.randint(1,5)
        lines[0] = str(infected_lines_number) + '\n'

    if 'content' in config['infeccion']:
        # una infeccion por linea
        #num_infections = len(num_lineas)-1
        texto_infeccion = ['__ERROR__','__HKED__','__KOMPROMISED__','__PWNED__','__XUNGOL__']

        for i in range(1,num_lineas+1):

            len_line = int(len(lines[i])/2)
            line_ini = lines[i][0:len_line]
            infeccion = random.choice(texto_infeccion)
            line_ini += infeccion
            infection_list.append((infeccion))
            line_ini += lines[i][len_line:]
            lines[i] = line_ini

    with open(filename, 'w') as f:
        f.writelines(lines)

    config['content_infections'] = infection_list





def build_filename(config):
    # Nombre
    final_name = ''
    dir_final = (config['dir_init'])
    for i in range(random.randint(1, 3)):
        dir_final = os.path.join(dir_final,random.choice(['d1', 'd2', 'd3']))

    # Extension
    extension = ''
    if len(config['infeccion']) == 0: # archivo sano
        extension = '.gen'
    elif 'ransom' == config['infeccion'][0]:
        extension = '.ransom'
    elif 'extension' in config['infeccion']:
        extension = '.' + random.choice(['error','pirate','pwned','bad'])
    else: # está infectado pero en size, auth o content
            # se manitiene la extensión original
        extension = '.gen'

    fname = 'data' + str(random.randint(0, 100)).zfill(3)

    final_name = os.path.join(dir_final,fname) + extension

    return final_name


def change_auth(config):


    # se añade por defceto el usuario recerca:gruprecerca
    user = 'recerca'
    cmd = f'useradd {user}'
    os.system(cmd)
    group = 'gruprecerca'
    cmd = f'groupadd {group}'
    os.system(cmd)
    import pwd
    if 'auth' in config['infeccion']:


        # escoge usuario al azar

        user_id = pwd.getpwnam('recerca').pw_uid
        while user_id == pwd.getpwnam('recerca').pw_uid:
            usuario = random.choice(pwd.getpwall())
            user_id = usuario.pw_uid
            group_id = usuario.pw_gid

        #print(os.stat(config['filename']))
        os.chown(config['filename'],user_id,group_id)
        #print(os.stat(config['filename']))
    else:
        user_id  = pwd.getpwnam(user).pw_uid
        import grp
        group_id = grp.getgrnam(group).gr_gid
        os.chown(config['filename'], user_id, group_id)


def create_file(config):


    filename = build_filename(config)
    config['filename']= filename
    print('filename en create',filename)

    # si por casualidad está dupllicado el nombre se sale
    if os.path.exists(filename):
        return

    # tamaño máximo 20KB
    size = random.randint(1, 20) * 1024 #

    # generar el nombre del archivo y sus posible infecciones que se guardan en config
    generate_file(filename,size,config)
    change_auth(config)

    if len(config['infeccion'])==0:
        print('>>>>>>>>>>>>>>> NO INFECTADO',filename)

        file_list_ok.append(filename)


    if len(config['infeccion'])>0:
        print('>>>>>>>>>>>>>>> INFECTADO',filename)
        print('>>>>CONFGIG',config)
        #guardar la lista de ficheros chungos si no es sano
        # si tiene ransom se deja solo ransom
        text = f'{filename}\t{config["infeccion"]}'
        file_list_chunga.append(text)
        if 'content_infections' in config and len(config['content_infections'])>0:
            file_list_chunga.append(' ' + f'    infecciones de contenido:{str(config["content_infections"])}\n')

    print('Procesado:',filename)




if __name__ == '__main__':
    if len(sys.argv) <2:
        print('necesito directorio inicial')
        sys.exit()


    for i in range(20):
        config = create_config()
        create_file(config)
        print()

 # VOLCADO FINAL DE DATOS PARA HACER TRAZAS
    from datetime import datetime
    ahora = datetime.now().strftime("%d-%m_%H-%M-%S")
    with open('output_simulacio_'+ahora + '.txt','a') as f:
        line = '-- LISTA INFECTADOS:\n'
        f.write(line)
        print(line.strip())
        for file in file_list_chunga:
            line = file + '\n'
            f.write(line)
            print(line.strip())



        line = '\n\n-- LISTA OK:\n'
        f.write(line)
        print(line.strip())
        for file in file_list_ok:
            line = file + '\n'
            f.write(line)
            print(line.strip())


        line = '\n\n-- LISTA RANSOM:\n'
        f.write(line)
        print(line.strip())
        for file in file_list_ransom:
            line = file + '\n'
            f.write(line)
            print(line.strip())



