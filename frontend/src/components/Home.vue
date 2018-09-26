<template>
<section class="container">
  <div class="my-4">
    <h1>Taggle</h1>
    <p>Find Kaggle competitions with various tags.</p>
    <input v-model="query" type="text" class="form-control" placeholder="Search">
  </div>
  <span v-if="loading">now loading...</span>
  <div class="list-group list-group-flush" v-if="!loading">
    <button class="list-group-item list-group-item-action justify-content-between" v-for="compe in filteredCompetitions" :key="compe.id">
      <div class="row">
        <div class="col-6">
          <img class="rounded float-left mr-2" :src="compe.image" alt="" width=60 height=60>
          <p><a :href="compe.url">{{compe.name}}</a><br><small>{{compe.startdate.format('YYYY-MM-DD')}} / {{compe.enddate.format('YYYY-MM-DD')}}</small></p>
        </div>
        <div class="col-5">
          <p><span v-for="tag in compe.tags.split(',')" :key="tag" class="badge badge-secondary m-1">{{tag}}</span></p>
        </div>
        <div class="col-1 text-right d-flex align-items-center justify-content-end"><span class="badge badge-light badge-pill">14</span></div>
      </div>
    </button>
  </div>
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
      const regs = this.query.split(/\s/).map(q => {
        return new RegExp(q.trim(), 'i')
      })
      return this.competitions.filter(compe => {
        return regs.every(reg => reg.test(compe.tags) || reg.test(compe.name))
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
