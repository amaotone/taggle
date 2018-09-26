<template>
<section class="container">
  <div class="my-4">
    <h1>Taggle</h1>
    <p>Find Kaggle competitions with various tags.</p>
    <input v-model="query" type="text" class="form-control" placeholder="search">
  </div>
  <span v-if="loading">now loading...</span>
  <table class="table table-sm" v-if="!loading">
    <tbody>
      <tr class="row" v-for="compe in filteredCompetitions" :key="compe.id">
        <td class="col-5">
          <img class="rounded float-left m-2" :src="compe.image" alt="" width=60 height=60>
          <a :href="compe.url">{{compe.name}}</a>
          <br>
          {{compe.startdate.format('YYYY-MM-DD')}} / {{compe.enddate.format('YYYY-MM-DD')}}
        </td>
        <td class="col-7"><span v-for="tag in compe.tags.split(',')" :key="tag" class="badge badge-dark m-1">{{tag}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
</template>

<script>
import db from './firebaseInit'
var moment = require('moment')
export default {
  name: 'home',
  data () {
    return {
      query: '',
      competitions: [],
      loading: true
    }
  },
  computed: {
    filteredCompetitions: function () {
      if (!this.query) return this.competitions
      const regs = this.query.split(',').map(q => {
        return new RegExp(q.trim())
      })
      return this.competitions.filter(compe => {
        return regs.every(reg => reg.test(compe.tags))
      })
    }
  },
  created () {
    db.collection('competitions').get().then((snapshot) => {
      this.loading = false
      snapshot.forEach((doc) => {
        let data = {
          'id': doc.id,
          'name': doc.data().name,
          'url': 'http://www.kaggle.com' + doc.data().url,
          'startdate': moment(doc.data().start),
          'enddate': moment(doc.data().end),
          'image': doc.data().image,
          'tags': Object.keys(doc.data().tags).join(',')
        }
        this.competitions.push(data)
      })
      this.competitions.sort((a, b) => b.startdate - a.startdate)
    })
  }
}
</script>
<style>
body {
  font-size: 14px;
}
</style>
