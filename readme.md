# Facultad de Ingeniería del Ejercito

## Proyecto Horus

### Simulador de eventos de Centros de Comunicaciones e Informática de Campaña

Este software genera eventos tipicos de la operacion de los CCIC de campaña y los permite ingresar a una instancia de
InfluxDB.

### Instalación

```bash
sudo apt install python3-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Buckets de eventos necesarios hasta ahora

- cola-cmd
- mensajes-ccic
- gpos-rtef

### TODO List

- [ ] Reportar a una API Horus.
- [ ] Generar datos de Sensores (V, A, Prescencia, Humo)
- [ ] Reportar F/S y E/S.
- [ ] Rechazar mensajes de acuerdo al estado de servicio.