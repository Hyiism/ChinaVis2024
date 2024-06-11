<template>
  <div id="table">
    <div class="search-container">
      <el-input 
        v-model="searchValue" size="mini" clearable
        placeholder="Search" style="width: 90%;" @keyup.enter="doFilter">
      </el-input>
      <el-button type="primary" size="mini" @click="doFilter">搜索</el-button>
    </div>
    <el-table :data="tableData" border @sort-change="handleSortChange">
      <el-table-column prop="student_ID" label="编号" align="center"></el-table-column>
      <el-table-column prop="sex" label="性别" align="center"></el-table-column>
      <el-table-column prop="age" label="年龄" align="center"></el-table-column>
      <el-table-column prop="major" label="专业" align="center"></el-table-column>
      <el-table-column prop="class" label="班级" align="center"></el-table-column>
      <el-table-column prop="total_score" label="总分" align="center" sortable="custom">
        <template slot="header" slot-scope="scope">
          <span>总分</span>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[1, 3, 4]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalItems"
        :pager-count="5"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      resData: [],
      searchValue: "",
      tableData: [],
      currentPage: 1,
      pageSize: 4,
      totalItems: 0,
      filterTableData: [],
      flag: false,
      sortField: '',
      sortOrder: '',
    };
  },
  mounted() {
    this.fetchStudentScores();
  },
  methods: {
    mockRequset() {
      this.totalItems = this.resData.length; 
      this.updateTableData();
    },
    fetchStudentScores() {
      this.$axios.get('http://10.12.44.190:8000/table/Class2')
        .then(response => {
          this.resData = JSON.parse(response.data).data;
          this.mockRequset();
          console.log("###table start###");
          console.log(this.resData);
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    doFilter() {
      this.filterTableData = [];
      this.resData.filter((item) => {
        if (item.student_ID && item.class && item.total_score && item.major && item.sex && item.age) {
          if (
            item.student_ID.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1 ||
            item.class.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1 ||
            item.total_score.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1 ||
            item.major.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1 ||
            item.sex.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1 ||
            item.age.toString().toUpperCase().indexOf(this.searchValue.toUpperCase()) > -1
          ) {
            this.filterTableData.push(item);
          }
        }
      });
      this.currentPage = 1;
      this.totalItems = this.filterTableData.length;
      this.flag = true;
      this.updateTableData();
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageSize = val;
      this.handleCurrentChange(1);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.currentPage = val;
      this.updateTableData();
    },
    updateTableData() {
      const list = this.flag ? this.filterTableData : this.resData;
      let fromNum = (this.currentPage - 1) * this.pageSize;
      let toNum = this.currentPage * this.pageSize;
      this.tableData = list.slice(fromNum, toNum);
    },
    handleSortChange({ prop, order }) {
      this.sortField = prop;
      this.sortOrder = order;
      const list = this.flag ? this.filterTableData : this.resData;
      if (order === 'ascending') {
        list.sort((a, b) => a[prop] - b[prop]);
      } else if (order === 'descending') {
        list.sort((a, b) => b[prop] - a[prop]);
      }
      this.updateTableData();
    }
  }
};
</script>

<style>
#table {
  width: 90%;
  margin: 0 auto;
  height: 90%;
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px; /* 调整这个值来增加与表格的距离 */
}

.el-input {
  margin-right: 10px; /* 调整这个值来增加搜索框和按钮之间的距离 */
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 调整这个值来增加与表格的距离 */
}

.el-icon-arrow-up,
.el-icon-arrow-down {
  cursor: pointer;
  margin-left: 5px;
  color: #909399;
}

.el-icon-arrow-up.active,
.el-icon-arrow-down.active {
  color: #409EFF;
}
</style>
