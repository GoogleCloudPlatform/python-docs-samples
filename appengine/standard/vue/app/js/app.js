'use strict';

var store = {
  debug:true,
  state: {
    guests:[]
  },
  setGuests:function (guests) {
    if (this.debug) console.log('setGuests triggered with');
    this.state.guests = guests
  },
  insertGuest: function (guest) {
    if (this.debug) console.log('insertGuest triggered with', guest);
    this.state.guests.push(guest)
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
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          })
    },
    invite:function(){
      window.location.href = '#/invite';
      window.location.reload();
    },
    remove:function(guest){
      var vm = this;
      //$rootScope.status = 'Deleting guest ' + guest.id + '...';
      axios.post('/rest/delete', {'id': guest.id})
          .then(function (response) {
            //$rootScope.status = '';
            vm.store.deleteGuest(guest);
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          });
    },
    update:function(guest){
      window.location.href = '#/update/' + guest.id;
      window.location.reload();
    },
  },
  mounted:function(){
    var vm = this; 
    vm.getList();
  },
};

const Insert = {
  template: `
  <div>
    <h2>Invite another guest</h2>
    <form @submit="submitInsert">
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
      //$rootScope.status = 'Creating...';
      axios.post('/rest/insert', guest)
          .then(function (response) {
            vm.store.insertGuest(response.data);
            window.location.href = '#/main';
            window.location.reload();
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
    <form @submit="submitUpdate">
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
  computed:{
    guest:function (){
      var vm = this; 
      var guest='',id; 

      window.location.hash;

      var url = window.location.hash.split('/'); 
      if(url.length === 3 && url[1] === 'update'){
        id = url[2];  
        for (var i=0; i<vm.store.state.guests.length; i++) {
          if (vm.store.state.guests[i].id == id) {
            guest = vm.store.state.guests[i];
          }
        }
      }
      
      return guest;
    }
  },
  methods: {
    submitUpdate:function() {
      var vm = this;
      //$rootScope.status = 'Creating...';
      axios.post('/rest/update', vm.guest)
          .then(function (response) {
            window.location.href = '#/main';
            window.location.reload();
          })
          .catch(function (error) {
            console.log(error)
            debugger;
          });
    }
  },
  beforeMount:function(){
    if(this.store.state.guests.length == 0){
      var vm = this
      axios.get('rest/query')
        .then(function (response) {
          vm.store.setGuests(response.data);
        })
        .catch(function (error) {
          console.log(error)
          debugger;
        })
    }
  },
};

var routes = {
  '': Main,
  '#/': Main,
  '#/main': Main,
  '#/invite': Insert,
  '#/update': Update,
}

new Vue({
  el: '#app',
  data: {
    currentRoute: window.location.hash,
  },
  computed: {
    ViewComponent () {
      var url = this.currentRoute.split('/'); 
      if(url.length === 3 && url[1] === 'update'){
        this.currentRoute = '#/update';
      }

      return routes[this.currentRoute] || NotFound
    }
  },
  render (h) { return h(this.ViewComponent) }
})


