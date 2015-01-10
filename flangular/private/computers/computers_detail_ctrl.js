angular.module('computers.detail', [])
.controller('ComputersDetailCtrl', [
             '$scope','$state','$stateParams','instance',
    function ($scope,  $state,  $stateParams,  instance) {
        $scope.model = instance('computer');
        $scope.model.$select($stateParams.id);

        $scope.create = function() {
            $state.go('computers.detail', {id: -1});
        };

        $scope.save = function() {
            $scope.model.$save().then(function() {
                console.log('DONE', $scope.model.id);
                $state.go('computers.detail', {id: $scope.model.id});
            });
        };

        $scope.remove = function() {
            $scope.model.$remove().then(function() {
                $state.go('computers.list');
            });
        };
    }
]);
