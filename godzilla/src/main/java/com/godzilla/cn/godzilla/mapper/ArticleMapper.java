package com.godzilla.cn.godzilla.mapper;

import com.godzilla.cn.godzilla.bean.Article;
import org.apache.ibatis.annotations.*;
import org.mybatis.spring.annotation.MapperScan;

import java.util.List;

@Mapper
public interface ArticleMapper {
    @Insert("INSERT INTO article(title,detail,nodes) VALUES(#{title},#{detail},#{nodes})")
    int add(@Param("title") String title, @Param("detail")String detail,@Param("nodes")String nodes);

    @Update("UPDATE article SET title = #{title}, detail = #{detail}, nodes = #{nodes} WHERE id = #{id}")
    int update(@Param("title") String title, @Param("detail") String detail, @Param("nodes") String nodes, @Param("id") Long  id);

    @Delete("DELETE FROM article WHERE id = #{id}")
    int delete(Long id);

    @Select("SELECT id, title, detail, nodes FROM article WHERE id = #{id}")
    Article findArticleById(@Param("id") Long id);

    @Select("SELECT id, title, nodes FROM article")
    List<Article> findArticleTitleList();

    @Select("SELECT id, title, detail, nodes FROM article")
    List<Article> findArticleList();
}
