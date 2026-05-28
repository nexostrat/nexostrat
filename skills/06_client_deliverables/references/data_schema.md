# Schema del archivo data_{empresa}.json

Este archivo es el input compartido para todos los scripts de generación. Créalo con cuidado — un campo mal formado causará errores en los scripts.

```json
{
  "metadata": {
    "empresa": "Nombre completo de la empresa",
    "empresa_slug": "NombreEmpresa (sin espacios, para nombres de archivo)",
    "sector": "Sector o industria",
    "ciudad": "Ciudad",
    "pais": "CO",
    "fecha_display": "28 de mayo de 2026",
    "fecha_iso": "2026-05-28",
    "consultor": "Ricardo [Apellido]",
    "consultor_email": "ricardo@nexostrat.co",
    "consultor_whatsapp": "+57 XXX XXX XXXX"
  },

  "empresa_hoy": {
    "descripcion": "Descripción narrativa de 2-3 párrafos del negocio. Usa el lenguaje que el cliente usa para describirse.",
    "metricas_clave": [
      "~50 empleados",
      "15 años en el mercado",
      "Operaciones en Bogotá y Medellín"
    ],
    "madurez_digital": "Básica | Media | Avanzada",
    "madurez_digital_descripcion": "Una línea explicando qué herramientas usan y dónde están digitalmente",
    "posicion_competitiva": "Descripción de 1-2 oraciones sobre su posición en el mercado"
  },

  "situacion_por_area": [
    {
      "area": "Ventas",
      "situacion_actual": "Cómo opera hoy esta área",
      "oportunidades": "Qué puede mejorar con IA"
    }
  ],

  "problemas": [
    {
      "id": 1,
      "titulo": "Cotizaciones manuales que tardan demasiado",
      "descripcion": "Descripción del problema en lenguaje de negocio. Impacto en la operación.",
      "cita_cliente": "Frase literal del cliente entre comillas, sin modificar. Si no hay cita exacta, la frase más cercana a cómo lo describió.",
      "costo_inaccion": {
        "descripcion": "Cada mes sin resolver esto equivale a ~X horas perdidas del equipo comercial",
        "metodo": "A | B | C",
        "calculo": "3 horas × 40 cotizaciones/mes = 120 horas/mes",
        "es_estimado": true
      }
    }
  ],

  "oportunidades": [
    {
      "id": 1,
      "titulo": "Automatización de cotizaciones",
      "problema_id": 1,
      "area": "Ventas",
      "descripcion": "Un sistema que genera cotizaciones automáticamente a partir de la descripción del pedido, lista de precios y condiciones comerciales del cliente.",
      "beneficio_esperado": "Reducir el tiempo de cotización de 3 horas a ~15 minutos. Liberar ~100 horas/mes del equipo comercial.",
      "categoria": "mediano",
      "horas_estimadas_implementacion": 40,
      "precio_usd_min": 10000,
      "precio_usd_max": 15000,
      "precio_nota": "40 horas × USD 250 = USD 10,000 mínimo. Rango mediano.",
      "requiere_infraestructura": true,
      "fee_mensual_usd": 100,
      "impacto_score": 4,
      "esfuerzo_score": 3,
      "quick_win": false
    }
  ],

  "quick_wins": [1, 2],

  "roadmap_fases": [
    {
      "fase": "Fase 1 — Quick Wins (0-3 meses)",
      "oportunidades_ids": [1, 2],
      "descripcion": "Iniciativas de alto impacto y menor complejidad para generar victorias rápidas"
    },
    {
      "fase": "Fase 2 — Consolidación (3-6 meses)",
      "oportunidades_ids": [3],
      "descripcion": "Iniciativas de mediana complejidad que construyen sobre los Quick Wins"
    },
    {
      "fase": "Fase 3 — Transformación (6-12 meses)",
      "oportunidades_ids": [4, 5],
      "descripcion": "Iniciativas más complejas que generan ventaja competitiva duradera"
    }
  ],

  "propuesta": {
    "total_roadmap_usd": 45000,
    "descripcion_total": "El valor total del roadmap completo (5 iniciativas) es de USD 45,000",
    "iniciativa_entrada_id": 1,
    "estructura_pago_descripcion": "El pago se divide en dos partes: un monto upfront al firmar (que confirma la intención y nos permite arrancar) y el saldo al finalizar la implementación. Esta estructura protege al cliente: solo paga el total cuando ve el resultado entregado y funcionando.",
    "upfront_porcentaje": 50,
    "garantia_descripcion": "1 mes de garantía post-implementación: soporte técnico incluido para ajustes y correcciones sin costo adicional."
  },

  "persuasion": {
    "quick_win_gancho_id": 1,
    "quick_win_gancho_razon": "Por qué este Quick Win es el mejor punto de entrada para este cliente específico",
    "cita_principal": "La cita más poderosa del cliente que captura el dolor central",
    "objecion_probable": "Descripción de la objeción más probable basada en las notas de Ricardo",
    "respuesta_objecion": "Cómo responder esa objeción en 2-3 oraciones concretas",
    "cta_sugerido": "Frase exacta para pedirle al cliente al terminar la presentación",
    "senales_positivas": [
      "El cliente expresó urgencia en el área X",
      "Ya evaluó otras opciones — está listo para decidir"
    ],
    "banderas_atencion": [
      "Presupuesto limitado — resaltar el ROI del Quick Win primero",
      "Equipo pequeño — enfatizar que la solución no requiere personal técnico interno"
    ]
  },

  "sobre_nexostrat": "Texto de máximo 150 palabras sobre la metodología de Nexostrat. Por qué entendimiento → diseño → validación → construcción entrega más que una consultora tradicional o un vendedor de software. Enfocado en ejecución, no en historia corporativa."
}
```

## Notas importantes

- `empresa_slug`: Sin espacios ni caracteres especiales. Ej: "Distribuidora Los Andes" → "DistribuidoraLosAndes"
- `categoria` de oportunidades: `"pequeno"` | `"mediano"` | `"grande"`
- `metodo` de costo de inacción: `"A"` (dato directo), `"B"` (analogía sectorial), `"C"` (razonamiento conservador)
- `quick_wins`: Array de IDs de las 2 oportunidades marcadas como Quick Win
- `upfront_porcentaje`: Normalmente 50. Puede variar según negociación.
- Los campos `precio_usd_max` pueden ser `null` si el precio es fijo (ej. proyectos pequeños = 3000, no hay rango)
