angular.module('computers', [
    'computers.list',
    'computers.detail'
])
.config(
     function ($stateProvider, $urlRouterProvider) {
         var templateUrl = function(url) {
             return '/priv/computers/' + url;
         };

         // $urlRouterProvider.when('/computers', '/computers/list');
         $stateProvider
             .state('computers', {
                 abstract: true,
                 url: '/computers',
                 templateUrl: templateUrl('computers.html')
             })
             .state('computers.list', {
                 url: '/list',
                 templateUrl: templateUrl('computers_list.html'),
                 controller: 'ComputersListCtrl'
             })
             .state('computers.detail', {
                 url: '/{id:int}',
                 templateUrl: templateUrl('computers_detail.html'),
                 controller: 'ComputersDetailCtrl'
             });
     }
);