'use strict';

var App = angular.module('App', ['ngRoute']);

App.factory('myHttpInterceptor', function($rootScope, $q) {
  return {
    'requestError': function(config) {
      $rootScope.status = 'HTTP REQUEST ERROR ' + config;
      return config || $q.when(config);
    },
    'responseError': function(rejection) {
      $rootScope.status = 'HTTP RESPONSE ERROR ' + rejection.status + '\n' +
                          rejection.data;
      return $q.reject(rejection);
    },
  };
});

App.factory('guestService', function($rootScope, $http, $q, $log) {
  $rootScope.status = 'Retrieving data...';
  var deferred = $q.defer();
  $http.get('rest/query')
  .success(function(data, status, headers, config) {
    $rootScope.guests = data;
    deferred.resolve();
    $rootScope.status = '';
  });
  return deferred.promise;
});

App.config(function($routeProvider) {
  $routeProvider.when('/', {
    controller : 'MainCtrl',
    templateUrl: '/partials/main.html',
    resolve    : { 'guestService': 'guestService' },
  });
  $routeProvider.when('/invite', {
    controller : 'InsertCtrl',
    templateUrl: '/partials/insert.html',
  });
  $routeProvider.when('/update/:id', {
    controller : 'UpdateCtrl',
    templateUrl: '/partials/update.html',
    resolve    : { 'guestService': 'guestService' },
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});

App.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});

App.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.invite = function() {
    $location.path('/invite');
  };

  $scope.update = function(guest) {
    $location.path('/update/' + guest.id);
  };

  $scope.delete = function(guest) {
    $rootScope.status = 'Deleting guest ' + guest.id + '...';
    $http.post('/rest/delete', {'id': guest.id})
    .success(function(data, status, headers, config) {
      for (var i=0; i<$rootScope.guests.length; i++) {
        if ($rootScope.guests[i].id == guest.id) {
          $rootScope.guests.splice(i, 1);
          break;
        }
      }
      $rootScope.status = '';
    });
  };

});

App.controller('InsertCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.submitInsert = function() {
    var guest = {
      first : $scope.first,
      last : $scope.last, 
    };
    $rootScope.status = 'Creating...';
    $http.post('/rest/insert', guest)
    .success(function(data, status, headers, config) {
      $rootScope.guests.push(data);
      $rootScope.status = '';
    });
    $location.path('/');
  }
});

App.controller('UpdateCtrl', function($routeParams, $rootScope, $scope, $log, $http, $location) {

  for (var i=0; i<$rootScope.guests.length; i++) {
    if ($rootScope.guests[i].id == $routeParams.id) {
      $scope.guest = angular.copy($rootScope.guests[i]);
    }
  }

  $scope.submitUpdate = function() {
    $rootScope.status = 'Updating...';
    $http.post('/rest/update', $scope.guest)
    .success(function(data, status, headers, config) {
      for (var i=0; i<$rootScope.guests.length; i++) {
        if ($rootScope.guests[i].id == $scope.guest.id) {
          $rootScope.guests.splice(i,1);
          break;
        }
      }
      $rootScope.guests.push(data);
      $rootScope.status = '';
    });
    $location.path('/');
  };

});

