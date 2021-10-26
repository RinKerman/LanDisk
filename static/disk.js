let app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            editVis: false,
            fileData: [],
            input: "",
            dir: "",
            newFolderName:"",
            createFolderVis: false,
            editFile: {},

        }
    },
    computed:{
        currDir(){return this.dir.substring(1, this.dir.length);}
    },
    methods: {
        flushData: function () {
            let self = this;
            axios.post('/listdir', {dir: self.currDir})
                .then(function (response) {
                    self.fileData = response.data.files;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        handleDownload: function (row) {
            debugger;
            let processedDir = this.currDir.replaceAll("/","$.$");
            window.open('/download?dir=' + processedDir + "&fileName=" + row.fileName);
        },
        handleEdit: function (row) {
            this.editFile = row;
            this.input = row.fileName;
            this.editVis = true;
        },
        doEditFileNm: function () {
            let self = this;
            self.editFile.newFileName = self.input;
            self.editFile.dir = self.currDir;
            axios.post('/edit', self.editFile)
                .then(function () {
                    self.$message({
                        type: 'success',
                        message: '已修改'
                    });
                    self.flushData();
                    self.editVis = false;
                }).catch(function (error) {
                this.$message({
                    type: 'error',
                    message: '错误'
                });
            });
        },

        handleDelete: function (row) {
            let self = this;
            let content = '此操作将永久删除该文件, 是否继续?';
            this.$confirm(content, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                doDelete(row);
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });

            function doDelete(row) {
                axios.post('/delete', {dir: self.currDir, fileName: row.fileName})
                    .then(function () {
                        self.$message({
                            type: 'success',
                            message: '已删除'
                        });
                        self.flushData();
                    })
                    .catch(function (error) {
                        self.$message({
                            type: 'error',
                            message: '无法删除，请确认文件夹是否为空'
                        });
                        self.flushData();
                    });
            }

        },
        handleSuccess: function (res) {
            if (res == '200') {
                this.$message({
                    message: '上传完成',
                    type: 'success'
                });
            } else {
                this.$message({
                    message: res,
                    type: 'error'
                });
            }

            this.flushData();
        },
        handleError: function (res) {
            this.$message({
                message: '上传失败',
                type: 'error'
            });
            this.flushData();
        },
        goToDir: function (dir) {
            this.dir = this.dir + '/' + dir;
            this.flushData();
        },
        stepBack: function () {
            let arr = this.dir.split("/");
            arr.splice(arr.length - 1, 1);
            this.dir = arr.join("/");
            this.flushData();
        },
        handleCreateFolder: function(){
            this.newFolderName = "";
            this.createFolderVis = true;
        },
        doCreateFolder: function(){
            let self = this;
            axios.post('/createDir', {dir: this.currDir, folderName: this.newFolderName})
                .then(function () {
                    self.createFolderVis = false;
                    self.$message({
                        type: 'success',
                        message: '创建完成'
                    });
                    self.flushData();
                })
                .catch(function (error) {
                    self.$message({
                        type: 'error',
                        message: '无法创建'
                    });
                    self.flushData();
                });
        }
    },
    mounted: function () {
        let self = this;
        this.flushData();
        setInterval(function () {
            self.flushData();
        }, 5000);
    }
});