'use strict';

var store = {
  debug:true,
  state: {
    status:'',
    guests:[],
  },
  setStatus: function (status) {
    this.state.status = status;
  },
  setGuests: function (guests) {
    if (this.debug) console.log('setGuests triggered with');
    this.state.guests = guests
  },
  insertGuest: function (guest) {
    if (this.debug) console.log('insertGuest triggered with', guest);
    this.state.guests.push(guest)
  },
  updateGuest: function(guest){
    if (this.debug) console.log('deleteGuest triggered with', guest);
    for (var i=0; i<this.state.guests.length; i++) {
      if (this.state.guests[i].id == guest.id) {
        this.state.guests[i] = guest;
        break;
      }
    }
  },
  deleteGuest: function (guest) {
    if (this.debug) console.log('deleteGuest triggered with', guest);
    for (var i=0; i<this.state.guests.length; i++) {
      if (this.state.guests[i].id == guest.id) {
        this.state.guests.splice(i, 1);
        break;
      }
    }
  },
}

const Main = {
  template: `
  <div>
    <h2>Guest list</h2>
    <button v-on:click="invite()">Invite another guest</button>
    <div v-for="(guest,index) in guests">
      <button v-on:click="remove(guest)">delete</button>
      <button v-on:click="update(guest)">update</button>
      {{ index + 1 }}. <b>{{ guest.first }} {{ guest.last }}</b>
    </div>
  </div>
  `,
  data: function () {
    return {
      store: store
    }
  },
  created () {
    // fetch the data when the view is created and the data is
    // already being observed
    this.fetchData()
  },
  computed:{
    guests:function (){
      return this.store.state.guests
    }
  },
  methods: {
    getList:function(){
      var vm = this
      axios.get('rest/query')
          .then(function (response) {
            vm.store.setGuests(response.data);
            vm.store.setStatus('');
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          })
    },
    invite:function(){
      this.$router.push('/invite')
    },
    remove:function(guest){
      var vm = this;
      vm.store.setStatus('Deleting guest ' + guest.id + '...');
      axios.post('/rest/delete', {'id': guest.id})
          .then(function (response) {
            vm.store.deleteGuest(guest);
            vm.store.setStatus('');
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          });
    },
    update:function(guest){
      this.$router.push('/update/'+guest.id)
    },
    fetchData:function(response){
      var vm = this; 
      vm.store.setStatus('Retrieving data...');
      if(vm.store.state.guests.length === 0){
        axios.get('rest/query')
          .then(function (response) {
            vm.store.setGuests(response.data);
            vm.store.setStatus('');
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          })
      } else {
        vm.store.setStatus('');
      }
    },
  },
};

const Insert = {
  template: `
  <div>
    <h2>Invite another guest</h2>
    <form @submit.prevent="submitInsert">
      <p>
        <label>First:</label>
        <input type="text" v-model="first" autofocus="true" />
      </p>
      <p>
        <label>Last:</label>
        <input type="text"  v-model="last" />
      </p>
      <input type="submit" class="btn" />
    </form>
  </div>
  `,
  data: function () {
    return {
      first:'',
      last:'',
      store: store
    }
  },
  methods: {
    submitInsert:function() {
      var vm = this;
      var guest = {
        first : vm.first,
        last : vm.last, 
      };
     
      vm.store.setStatus('Creating...');
      axios.post('/rest/insert', guest)
          .then(function (response) {
            vm.store.insertGuest(response.data);
            vm.store.setStatus('');
            vm.$router.push('/')
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          });
    }
  },
};

const Update = {
  template: `
  <div>
    <h2>Update guest information</h2>
    <form @submit.prevent="submitUpdate">
      <p>
        <label>Id:</label>
        <input type="text" v-model="guest.id" disabled="true" />
      </p>
      <p>
        <label>First:</label>
        <input type="text" v-model="guest.first" autofocus="true" />
      </p>
      <p>
        <label>Last:</label>
        <input type="text"  v-model="guest.last" />
      </p>
      <input type="submit" class="btn" />
    </form>
  </div>
  `,
  data: function () {
    return {
      store: store
    }
  },
  created () {
    // fetch the data when the view is created and the data is
    // already being observed
    this.fetchData()
  },
  computed:{
    guest:function (){
      var vm = this; 
      var guest='',id; 
      id = this.$route.params.id; 

      for (var i=0; i<vm.store.state.guests.length; i++) {
        if (vm.store.state.guests[i].id == id) {
          guest = vm.store.state.guests[i];
          break;
        }
      }
      return guest;
    }
  },
  methods: {
    submitUpdate:function() {
      var vm = this;
      vm.store.setStatus('Updating...');
      axios.post('/rest/update', vm.guest)
        .then(function (response) {
          vm.store.updateGuest(vm.guest);
          vm.store.setStatus('');
          vm.$router.push('/')
        })
        .catch(function (error) {
          console.log(error)
          debugger;
        });
    }, 
    fetchData:function(response){
      var vm = this; 
      vm.store.setStatus('Retrieving data...');
      if(vm.store.state.guests.length === 0){
        axios.get('rest/query')
          .then(function (response) {
            vm.store.setGuests(response.data);
            vm.store.setStatus('');
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          })
      } else {
        vm.store.setStatus('');
      }
    },
  },
};

const routes = [
  { path: '/', component: Main },
  { path: '/invite', component: Insert},
  { path: '/update/:id', component: Update }
]

const router = new VueRouter({
  routes // short for `routes: routes`
})

new Vue({
  el: '#app',
  router, // short for `router: router`
  data: function () {
    return {
      store: store
    }
  },
  computed:{
    status: function(){
      return this.store.state.status;
    }
  }
})


