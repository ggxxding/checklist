<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>

</template>

<script>
  import axios from 'axios';
  export default {
    name: 'Ping',
    data() {
      return {
        msg: 'no',
      };
    },
    methods: {
      getMessage() {
        const path = 'http://localhost:5000';
        axios(
          {method:'post',
          url:path,
          data:{
            name:'name'
          }})
          .then((res) => {
            console.log(123)
            this.msg = res.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
    },
    created() {
      this.getMessage();
    }
  };
</script>
