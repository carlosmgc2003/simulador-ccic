# Facultad de Ingeniería del Ejercito

## Proyecto Horus

### Simulador de eventos de Centros de Comunicaciones e Informática de Campaña

Este software genera eventos tipicos de la operacion de los CCIC de campaña y los permite ingresar a una instancia de
InfluxDB.

### Instalación

```bash
git clone https://bitbucket.org/proyecto-horus/simulador-ccic.git
cd simulador-ccic
sudo apt install python3-virtualenv
virtualenv venv
source venv/bin/activate
(venv) pip install -r requirements.txt
```
### Utilizacion
Verificar que el archivo config.ini contenga las variables correctas para la instancia del sistema Horus que se encuentra en ejecucion.
```bash
(venv) python simular.py
```
El sistema correra un ciclo completo y finalmente vaciara los mensajes insertados en la BD Eventos.


### TODO List

- [X] Reportar a una API Horus.
- [ ] Generar datos de Sensores (V, A, Prescencia, Humo)
- [X] Reportar F/S y E/S.
- [ ] Rechazar mensajes de acuerdo al estado de servicio.