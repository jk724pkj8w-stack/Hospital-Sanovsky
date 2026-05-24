<template>
  <div class="register container mt-5">
    <h1 class="mb-4 text-center">Crear cuenta nueva</h1>
    <form @submit.prevent="registrarUsuario" class="card p-4 shadow-sm">
      <div class="form-group mb-3">
        <label for="nombre">Nombre completo</label>
        <input type="text" id="nombre" v-model="nombre" required class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="email">Correo electrónico</label>
        <input type="email" id="email" v-model="email" required class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="password">Contraseña</label>
        <input type="password" id="password" v-model="password" required class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="rol">Rol</label>
        <select id="rol" v-model="rol" required class="form-control">
          <option value="">Seleccione un rol</option>
          <option value="paciente">Paciente</option>
          <option value="doctor">Doctor</option>
          <option value="admin">Administrador</option>
        </select>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>
      <button type="submit" class="btn btn-success w-100">Registrar</button>
    </form>
  </div>
</template>

<script>
import { auth } from "../firebase"; // Asegúrate de importar la configuración de Firebase
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth";

export default {
  name: 'Register',
  data() {
    return {
      nombre: '',
      email: '',
      password: '',
      rol: '',
      error: '',
      success: ''
    };
  },
  methods: {
    async verificarCorreoExistente(correo) {
      const response = await fetch(`http://192.168.17.2:7777/getValidaEmail/${correo}`);
      const data = await response.json();
      return data.existente;
    },
    async registrarUsuario() {
      this.error = '';
      this.success = '';

      if (this.password.length < 6) {
        this.error = 'La contraseña debe tener al menos 6 caracteres.';
        return;
      }

      const correoExiste = await this.verificarCorreoExistente(this.email);
      if (correoExiste) {
        this.error = 'El correo ya está registrado en el sistema.';
        return;
      }

      try {
        const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password);
        await updateProfile(userCredential.user, { displayName: this.nombre });

        await fetch("http://192.168.17.2:7777/usuarios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            nombre: this.nombre,
            correo: this.email,
            rol: this.rol
          })
        });

        localStorage.setItem('justRegistered', 'true');
        this.success = 'Usuario registrado con éxito.';
        setTimeout(() => {
          this.$router.push('/login');
        }, 1500);
      } catch (error) {
        console.error("Error al registrar usuario:", error.message);
        this.error = 'No se pudo registrar el usuario. ' + error.message;
      }
    }
  }
}
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
}
</style>