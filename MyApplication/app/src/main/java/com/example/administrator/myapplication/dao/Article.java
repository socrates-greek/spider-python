package com.example.administrator.myapplication.dao;

public class Article {

    public long id;
    public String title;
    public String detail;
    public String nodes;
    public long  userArticleId;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDetail() {
        return detail;
    }

    public void setDetail(String detail) {
        this.detail = detail;
    }

    public String getNodes() {
        return nodes;
    }


    public void setNodes(String nodes) {
        this.nodes = nodes;
    }

    public long getUserArticleId() {
        return userArticleId;
    }

    public void setUserArticleId(long userArticleId) {
        this.userArticleId = userArticleId;
    }
}

