<template>
  <div class="home">
    <h1 class="headline">
      Want to get influenced or influence others? Start your journey now!
    </h1>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>

<style>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  background: linear-gradient(135deg, #f3f4f6, #d9e3f0);
  padding: 20px;
  text-align: center;
}

.headline {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0;
  max-width: 800px;
  line-height: 1.3;
}

.headline::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background-color: #007bff;
  margin: 20px auto 0;
}
</style>
