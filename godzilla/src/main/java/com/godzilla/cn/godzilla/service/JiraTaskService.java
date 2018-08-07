package com.godzilla.cn.godzilla.service;

import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.JiraTask;

import java.util.List;

public interface JiraTaskService {
    int add(JiraTask jiraTask);
    int delete(Long id);
    JiraTask findJiraTaskById(Long id);
    List<JiraTask> findAllList();

}
