# Facultad de Ingeniería del Ejercito

## Proyecto Horus

### Simulador de eventos de Centros de Comunicaciones e Informática de Campaña

Este software genera eventos tipicos de la operacion de los CCIC de campaña y los permite ingresar a una instancia de contenedores del sistema Horus - Tablero de control

### Instalación

```bash
git clone https://proyecto-horus-admin@bitbucket.org/proyecto-horus/simulador-ccic.git
cd simulador-ccic
sudo apt install python3-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecución
Con el sistema Horus Tablero de Control corriendo:
```bash
(venv) $ python main.py
```
En caso de tener sistema Horus Tablero de Control en otro host, se deberá cambiar los parametros del archivo config.ini apuntando a las direccion http de la api Horus 