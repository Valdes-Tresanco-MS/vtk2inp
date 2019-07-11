import argparse, os, sys

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="VTK file to convert",
                    type=argparse.FileType(mode='r'), required=True)
parser.add_argument('-o', '--output', help="Output file. Default = output.inp",
                    default='output.inp')

args = parser.parse_args()

print('Processing...')

points_data = []
cell_data = []

vtk_file = args.file

nline = 0
add = True
for line in vtk_file:
    nline += 1
    line = line.strip('\n')
    if len(line.split()) == 0:
        nline -=1
        continue
    if line.startswith('#'):
        file_version = line[1:].strip()
        continue
    if 'vtk output' in line:
        continue
    if nline == 2:
        title = line.strip()
        continue
    if nline == 3:
        if line.strip() in ['ASCII', 'BINARY']:
            file_type = line.strip()
        continue
    if nline == 4:
        data_set = line.split()[1].strip()
        continue
    if line.startswith('POINTS'):
        points = line.split()[1].strip()
        points_type = line.split()[2].strip()
        continue

    if 'CELLS' in line:
        add = False
        continue

    if 'CELL_DATA' in line or 'CELL_TYPE' in line:
        break

    if add:
        if len(line.split()) == 3:
            points_data.append(line.split())
        elif len(line.split()) == 6:
            points_data.append(line.split()[:3])
            points_data.append(line.split()[3:6])
        elif len(line.split()) == 9:
            points_data.append(line.split()[:3])
            points_data.append(line.split()[3:6])
            points_data.append(line.split()[6:9])
        else:
            # pass
            raise IOError('The number of coordinate elements is not a factor of '
                          '3!!!. Please check this.')
    else:
        if line.split():
            cell_data.append(line.split()[1:])

print('Converting VTK file ( %s ):\nTITLE: %s\nVTK DATA VERSION: %s\nFILE_TYPE: '
      '%s\nPOINTS: %s\nCELLS: %s' % (os.path.split(args.file.name)[1],title,
                                     file_version.split()[-1],file_type,points,
                                     len(cell_data)))

if os.path.exists(args.output):
    replace = input('%s already exists!!!. Do you want to replace it? [y/N]: '
                    % args.output)
    if replace.strip().lower() in ['t', 'true','y','yes', 's','si']:
        output_file = open(args.output,'w')
    else:
        print('User process aborted!!!. Exiting...')
        sys.exit(1)
else:
    output_file = open(args.output, 'w')


print('Writing %s...' % output_file.name)
output_file.write('** ' + 77 * '*' + '\n')
output_file.write('**  Written by ...\n')
output_file.write('** ' + 77 * '*' + '\n')
output_file.write('*NODE, NSET=GLOBAL\n')
ndat = 1
for data in points_data:
    output_file.write(('%s,' % ndat).rjust(9) + ('%s,' % data[0]).rjust(13) + ('%s,' % data[1]).rjust(13) +
                      ('%s' % data[2]).rjust(12) + '\n')
    ndat += 1
output_file.write('*ELEMENT, TYPE=C3D8, ELSET=P1\n')
ndat = 1
for data in cell_data:
    output_file.write(('%s,' % ndat).rjust(8) + ('%s,' % (int(data[0]) + 1)).rjust(8) + ('%s,' % (int(data[1]) + 1)).rjust(8) +
                      ('%s,' % (int(data[2]) + 1)).rjust(8) + ('%s,' % (int(data[3]) + 1)).rjust(8) + ('%s,' % (int(data[4]) + 1)).rjust(8) +
                      ('%s,' % (int(data[5]) + 1)).rjust(8) + ('%s,' % (int(data[6]) + 1)).rjust(8) + ('%s' % (int(data[7]) + 1)).rjust(8) + '\n')
    ndat += 1

output_file.write('*ELSET, ELSET=OUT_CONT, GENERATE\n1,%s,1 \n' % len(cell_data) +
                  '*SOLID SECTION, ELSET=P1, MATERIAL=M1\n** NX Nastran for FEMAP Property 2 : P3\n' +
                  '*ORIENTATION, NAME=S0, DEFINITION=COORDINATES, SYSTEM=RECTANGULAR\n' +
                  '        1.,        0.,        0.,        0.,        1.,        0.\n' +
                  '*SOLID SECTION, ELSET=P2, MATERIAL=M1, ORIENTATION=S0\n' +
                  '** NX Nastran for FEMAP Material 1 : M1\n' + '*MATERIAL, NAME=M1\n' + '*ELASTIC, TYPE=ISOTROPIC\n' +
                  '        0.,        0.,        0.\n' + '** NX Nastran for FEMAP Material 2 : M2\n' +
                  '*MATERIAL, NAME=M2\n' + '*ELASTIC, TYPE=ISOTROPIC\n' + '        0.,        0.,        0.\n' +
                  '** Load Step 1 -------------------------------------------------------\n' +
                  '*STEP, INC=100\n' + 'Untitled\n' + '*STATIC\n\n' + '*NODE PRINT, FREQUENCY=1\n' + '    U,\n' +
                  '*FILE FORMAT, ASCII\n' + '*NODE FILE, FREQUENCY=1\n' + '    U,\n' + '*NODE FILE, FREQUENCY=1\n' +
                  '   CF,\n' + '*NODE FILE, FREQUENCY=1\n' + '   RF,\n' +
                  '*EL PRINT, ELSET=OUT_CONT,FREQUENCY=1, POSITION=CENTROIDAL\n' + '    S,\n' + ' SINV,\n' +
                  '*EL PRINT, ELSET=OUT_CONT,FREQUENCY=1,	POSITION=NODES\n' + '    S,\n' + ' SINV,\n' +
                  '*EL FILE, ELSET=OUT_CONT,FREQUENCY=1, POSITION=CENTROIDAL\n' + '    S,\n' + ' SINV,\n' +
                  '*EL FILE, ELSET=OUT_CONT,FREQUENCY=1,	POSITION=NODES\n' + '    S,\n' + ' SINV,\n' +
                  '*EL PRINT, ELSET=OUT_CONT,FREQUENCY=1, POSITION=CENTROIDAL\n' +
                  '*EL PRINT, ELSET=OUT_CONT,FREQUENCY=1,	POSITION=NODES\n' +
                  '*EL FILE, ELSET=OUT_CONT,FREQUENCY=1, POSITION=CENTROIDAL\n' +
                  '*EL FILE, ELSET=OUT_CONT,FREQUENCY=1,	POSITION=NODES\n' + '*END STEP\n')
output_file.close()
print('Done...')