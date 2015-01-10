angular.module('computers.list', [])
.controller('ComputersListCtrl', [
             '$scope','collection','$state',
    function ($scope,  collection,  $state) {
        $scope.model = collection('computer');
        $scope.model.load();

        $scope.create = function() {
            $state.go('computers.detail', {id: -1});
        };

        $scope.edit = function(rowid) {
            $state.go('computers.detail', {id: rowid});
        };
    }
]);
