<template>
<section class="container">
  <div class="my-4">
    <h1>Taggle</h1>
    <p>Find Kaggle competitions with various tags.</p>
    <input v-model="query" type="text" class="form-control" placeholder="Search">
  </div>
  <span v-if="loading">Now Loading...</span>
  <div class="list-group" v-if="!loading">
    <button class="list-group-item list-group-item-action" v-for="compe in filteredCompetitions" :key="compe.id" @click="compe.showLinks = !compe.showLinks">
      <div class="row">
        <div class="col-6 d-flex justify-content-start align-items-start">
          <div class="align-self-start mr-2"><img class="rounded" :src="compe.image" alt="" width=60 height=60></div>
          <div class="align-self-start"><p><a :href="compe.url">{{compe.name}}</a><br><small>{{compe.startdate.format('YYYY-MM-DD')}} / {{compe.enddate.format('YYYY-MM-DD')}}</small></p></div>
        </div>
        <div class="col-5">
          <p><span v-for="tag in compe.tags" :key="tag" class="badge badge-dark mr-2">{{tag}}</span><a href="#"><ion-icon name="create"></ion-icon></a></p>
        </div>
        <div class="col-1 text-right d-flex align-items-center justify-content-end">
          <span class="badge badge-light badge-pill">0</span>
          </div>
      </div>
      <div v-if="compe.showLinks">
        <ul class="list-group pt-2">
          <li class="list-group-item">
            <a href="#">1st place solution</a>
            <span class="badge badge-dark mx-1">table</span>
          </li>
          <li class="list-group-item">
            <a href="#">1st place solution</a>
            <span class="badge badge-dark mx-1">table</span>
          </li>
        </ul>
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
        return regs.every(reg => reg.test(compe.searchTarget))
      })
    }
  },
  created () {
    db.collection('competitions').get().then((snapshot) => {
      snapshot.forEach((doc) => {
        let data = {
          'id': doc.id,
          'name': doc.data().name,
          'url': 'http://www.kaggle.com' + doc.data().url,
          'startdate': moment(doc.data().start),
          'enddate': moment(doc.data().end),
          'image': doc.data().image,
          'tags': Object.keys(doc.data().tags),
          'showLinks': false
        }
        data['searchTarget'] = data['name'] + ' ' + data['tags'].join(' ')
        this.competitions.push(data)
      })
      this.competitions.sort((a, b) => b.startdate - a.startdate)
      this.loading = false
    })
  }
}
</script>
<style>
body {
  font-size: 14px;
}
</style>
