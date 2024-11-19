import subprocess

# Solicita o nome da indústria
indústria = input('Qual indústria está conciliando? (organon, msd, sanofi, apsen, bayer): ').lower()

# Verifica qual indústria foi inserida e executa o script correspondente
if indústria == 'organon':
    distribuidor = input('Qual o distribuidor? (Digite GSC): ').upper()
    if distribuidor == 'GSC':
        subprocess.run(["python", "scripts/conciliação_organon_gsc.py"])
    else:
        print(f"Distribuidor não reconhecido ou não automatizado para a indústria {indústria}.")

#elif indústria == 'sanofi':
#    distribuidor = input('Qual o distribuidor? ')
#    subprocess.run(["python", "scripts/sanofi.py"])

elif indústria == 'apsen':
    distribuidor = input('Qual o distribuidor? (DIMED, GAM, GSC, GJB): ').upper()
    if distribuidor == 'DIMED':
        subprocess.run(['python', 'scripts/conciliação_apsen_dimed.py'])
    elif distribuidor == 'GAM':
        subprocess.run(['python', 'scripts/conciliação_apsen_gam.py'])
    elif distribuidor == 'GJB':
        subprocess.run(['python', 'scripts/conciliação_apsen_gjb.py'])
    elif distribuidor == 'GSC':
        print('Devido o tamanho do arquivo, apenas as chaves do relatório de ressarcimento serão feitas.')
        subprocess.run(['python', 'scripts/conciliação_apsen_gsc.py'])
    else:
        print(f"Distribuidor não reconhecido ou não automatizado para a indústria {indústria}.")

elif indústria == 'msd':
    distribuidor = input('Qual distribuidor? (GSC, AGILLE): ').upper()
    if distribuidor == 'GSC':
        subprocess.run(['python', 'scripts/conciliação_msd_gsc.py'])
    elif distribuidor == 'AGILLE':
        subprocess.run(['python', 'scripts/conciliação_msd_agille.py'])
    
    else:
        print(f"Distribuidor não reconhecido ou não automatizado para a indústria {indústria}.")
else:
        print(f"Indústria {indústria} não reconhecida ou não automatizada.")