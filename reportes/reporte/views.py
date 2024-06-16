from django.http import JsonResponse
from .models import Visit
import pandas as pd
from datetime import datetime

def reporte_atenciones(request):
    # Obtener todas las atenciones completadas
    atenciones = Visit.objects.filter(status='COMPLETADO')

    # Convertir las atenciones a un DataFrame de Pandas
    data = [{
        'fecha': Visit.date,
        'reserva': Visit.reserved,
    } for Visit in atenciones]
    df = pd.DataFrame(data)

    # Contar las reservas y atenciones sin cita por día
    df['fecha'] = pd.to_datetime(df['fecha'])
    reservas_por_dia = df[df['reserva']].groupby(df['fecha'].dt.date).size()
    sin_reserva_por_dia = df[~df['reserva']].groupby(df['fecha'].dt.date).size()

    # Crear un DataFrame con las dos series
    df_resumen = pd.DataFrame({
        'Reservas': reservas_por_dia,
        'Sin Reserva': sin_reserva_por_dia
    }).fillna(0)

    # Convertir los datos a un diccionario para JSON
    data = {
        'fechas': df_resumen.index.strftime('%Y-%m-%d').tolist(),
        'reservas': df_resumen['Reservas'].tolist(),
        'sinReserva': df_resumen['Sin Reserva'].tolist()
    }

    return JsonResponse(data)
