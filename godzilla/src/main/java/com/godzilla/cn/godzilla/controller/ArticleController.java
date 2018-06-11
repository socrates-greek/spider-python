package com.godzilla.cn.godzilla.controller;


import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.User;
import com.godzilla.cn.godzilla.service.ArticleService;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping(value="/article")     // 通过这里配置使下面的映射都在/users下，可去除
public class ArticleController {

    @Autowired
    public ArticleService articleService;

    @ApiOperation(value="获取文章章节列表", notes="")
    @RequestMapping(value={"/getArticleTitleList"}, method=RequestMethod.GET)
    public List<Article> getArticleTitleList() {
        List<Article> art = new ArrayList<>();
        art = articleService.findArticleTitleList();
        return art;
    }

    @ApiOperation(value="插入文章", notes="根据对象创建用户")
    @ApiImplicitParam(name = "article", value = "详细实体user", required = true, dataType = "Article")
    @RequestMapping(value="/addArticle", method=RequestMethod.POST)
    public String postUser(@RequestBody Article article) {
        articleService.add(article.getTitle(),article.getDetail(),article.getNodes());

        return "success";
    }

    @ApiOperation(value="获取详细信息", notes="根据url的id来获取详细信息")

    @ApiImplicitParam(name = "id", value = "ID", required = true, dataType = "Long")
    @RequestMapping(value="/getArticle/{id}", method=RequestMethod.GET)
    public Article getArticle(@PathVariable Long id) {
        return articleService.findArticleById(id);
    }

    @ApiOperation(value="更新详细信息", notes="根据url的id来指定更新对象，并根据传过来的user信息来更新用户详细信息")
    @ApiImplicitParams({
            @ApiImplicitParam(name = "id", value = "ID", required = true, dataType = "Long"),
            @ApiImplicitParam(name = "article", value = "详细实体", required = true, dataType = "Article")
    })
    @RequestMapping(value="/modifyArticle/{id}", method=RequestMethod.PUT)
    public String putArticle(@PathVariable Long id, @RequestBody Article article) {
        Article u = articleService.findArticleById(id);
        u.setTitle(article.getTitle());
        u.setDetail(article.getDetail());
        u.setNodes(article.getNodes());
        articleService.update(u.getTitle(),u.getDetail(),u.getNodes(),u.getId());

        return "success";
    }

    @ApiOperation(value="删除", notes="根据url的id来指定删除对象")
    @ApiImplicitParam(name = "id", value = "ID", required = true, dataType = "Long")
    @RequestMapping(value="/deleteArticle/{id}", method=RequestMethod.DELETE)
    public String deleteArticle(@PathVariable Long id) {
        articleService.delete(id);
        return "success";
    }

}
