package com.godzilla.cn.godzilla.mapper;

import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.JiraTask;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface JiraTaskMapper {
    @Insert("INSERT INTO jiratask (issuekey,description,reaction,summary,reporter,status,issuetype,details,state,createtime) values (#{issuekey},#{descrip},#{reaction},#{summary},#{reporter},#{status},#{issueType},#{details},#{state},#{createTime})")
    int add(JiraTask jiraTask) throws Exception;

    @Delete("UPDATE jiratask SET state = '1' WHERE id = #{id}")
    int delete(Long id);

    @Select("SELECT * FROM jiratask WHERE id = #{id}")
    JiraTask findJiraTaskById(@Param("id") Long id);

    @Select("SELECT * FROM jiratask WHERE state = '0'")
    List<JiraTask> findAllList();

}
