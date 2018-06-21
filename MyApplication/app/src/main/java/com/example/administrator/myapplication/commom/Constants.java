package com.example.administrator.myapplication.commom;

public class Constants {


    //public static String ip ="127.0.0.1";
    public static String ip ="140.143.230.126";
    public static String port ="8080";
    public static String ArticleTitleList ="http://"+ip+":"+port+"/article/getArticleTitleList";
    public static String ArticleById ="http://"+ip+":"+port+"/article/getArticle/";
    //根据用户id获取文章列表
    public static String findAllByuserId ="http://"+ip+":"+port+"/article/findAllByuserId/";
    //删除文章
    public static String deleteUserArticle= "http://"+ip+":"+port+"/article/deleteUserArticle/";

    //设置已读
    public static String modifyRead= "http://"+ip+":"+port+"/article/modifyRead/";
    //登录校验
    public static String UserByCountAndPassword ="http://"+ip+":"+port+"/users/getUserByCountAndPassword";


}
