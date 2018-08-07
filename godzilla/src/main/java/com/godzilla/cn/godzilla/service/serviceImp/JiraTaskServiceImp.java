package com.godzilla.cn.godzilla.service.serviceImp;

import com.godzilla.cn.godzilla.bean.JiraTask;
import com.godzilla.cn.godzilla.mapper.JiraTaskMapper;
import com.godzilla.cn.godzilla.service.JiraTaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class JiraTaskServiceImp implements JiraTaskService {

    @Autowired
    private JiraTaskMapper jiraTaskMapper;

    @Override
    public int add(JiraTask jiraTask) {
        int i = 0;
        try {
            i = jiraTaskMapper.add(jiraTask);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return i;
    }

    @Override
    public int delete(Long id) {
        return jiraTaskMapper.delete(id);
    }

    @Override
    public JiraTask findJiraTaskById(Long id) {
        return jiraTaskMapper.findJiraTaskById(id);
    }

    @Override
    public List<JiraTask> findAllList() {
        return jiraTaskMapper.findAllList();
    }
}


