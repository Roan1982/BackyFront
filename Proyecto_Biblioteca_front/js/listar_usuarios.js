const url = 'http://127.0.0.1:5000/usuarios';

fetch(url)
  .then(response => response.json())
  .then(data => {
    const usuariosLista = document.getElementById('usuarios-lista');
    data.forEach(usuario => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${usuario.id_usuario}</td>
        <td>${usuario.nombre}</td>
        <td>${usuario.apellido}</td>
        <td>${usuario.username || '-'}</td>
        <td>${usuario.email}</td>
        <td>${usuario.fecha_nacimiento || '-'}</td>
        <td>${usuario.fecha_registro || '-'}</td>
        <td>${usuario.genero || '-'}</td>
        <td>${usuario.pais || '-'}</td>
        <td>${usuario.rol ? usuario.rol : '-'}</td>
        <!-- Puedes agregar más celdas según los campos que desees mostrar -->
      `;
      usuariosLista.appendChild(tr);
    });
  })
  .catch(error => console.error('Error fetching usuarios:', error));
