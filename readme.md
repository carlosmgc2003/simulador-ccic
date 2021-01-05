# Facultad de Ingeniería del Ejercito

## Proyecto Horus

### Simulador de eventos de Centros de Comunicaciones e Informática de Campaña

Este software genera eventos tipicos de la operacion de los CCIC de campaña y los permite ingresar a una instancia de
InfluxDB.
`TODO: Que los ingrese a una API Horus`
> Para tener una instancia de influx en docker:
`docker run --name influxdb -p 8086:8086 quay.io/influxdb/influxdb:v2.0.3`

### Buckets de eventos necesarios hasta ahora

- cola-cmd
- mensajes-ccic
- gpos-rtef

### TODO List

- [ ] Reportar a una API Horus.
- [ ] Generar datos de Sensores (V, A, Prescencia, Humo)
- [ ] Reportar F/S y E/S.
- [ ] Rechazar mensajes de acuerdo al estado de servicio.