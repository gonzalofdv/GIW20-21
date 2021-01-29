# GIW20-21
Prácticas de Gestión de la Información Web

Universidad Complutense de Madrid - Facultad de Informática

## Notas de cada práctica

**Practica 1**: 9'5/10

**Practica 2**: 10/10

**Practica 3**: 9'5/10

**Practica 4**: 9'5/10

**Practica 5**: 10/10

**Practica 6**: 10/10

**Practica 7**: 9/10

**Practica 8**: 9/10

**Practica 9**: 10/10

**Practica 10**: 10/10

**Practica 11**:

**Practica 12**:

## Retroalimentación de las correcciones

**Practica 1**

En el ejercicio 3 solo se tiene en cuenta los casos de separados al final de las palabras.

**Practica 7**

- Pasa 16 de los 17 tests. Falla en el test "test_patch_asignatura_mal_formada"
- Buena idea la de definir comprobarDict() y usarla allí donde hay que comprobar diccionarios bien formados
- ¿Por qué usáis "None" en lugar de None? El valor nulo en Python debe ser None, no una cadena de texto. Además, se debe compara con "is": "pagina is not None", "pagina is None"
- id() es una función predeterminada de Python que devuelve la identidad de un objeto. Definís la variable "id" y eso oculta la función predeterminada.

**Práctica 8**

	
- Falla en 1 de los 12 tests de unidad, concretamente en test_inserta(). ¿Por qué creáis usuarios con una fecha de nacimiento (f_nac="1998, 3, 1") que no cumple con vuestro formato definido? Si se usa el formato con separadores "-" funciona correctamente.
- La cabecera debe indicar la asignatura, la práctica, el grupo y los autores
- El modulo Python NO DEBE INVOCAR AUTOMÁTICAMENTE A inserta(), únicamente definir las clases y los métodos
- En clean() de Pedido usáis una lista productos para comprobar repetidos => debería ser un conjunto

**Práctica 9**

1. Autenticación básica mediante contraseñas: 4pt
 * Usa HASH seguro
 * Usa sal
 * Usa ralentizado (¡incluso demasiado lento!)
2. Autenticación con TOTP: 6pt
 * Incrusta QR en HTML, muy buena elección

**Práctica 10**

- Utiliza token antiCSRF, bien hecho
- Autenticación correcta: sí
- Utiliza el documento de descubrimiento: sí
