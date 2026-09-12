# -*- coding: utf-8 -*-
"""生成示例元数据 data/import.json（模拟从公开渠道抓取的会议日程与资料元数据）。"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def sp(name, aff, bio=''):
    return {'name': name, 'affiliation': aff, 'bio': bio}

def fl(title, ftype, filename, fmt, size_kb, pages=0, lang='中文', uploaded='', status='active', block_reason=''):
    return {'title': title, 'file_type': ftype, 'filename': filename, 'format': fmt,
            'size_kb': size_kb, 'pages': pages, 'language': lang, 'uploaded_at': uploaded,
            'source_url': 'https://files.example.org/' + filename,
            'status': status, 'block_reason': block_reason}

def sess(day, track, title, room, st, et, abstract, speakers, files):
    return {'day': day, 'track': track, 'title': title, 'room': room,
            'start_time': st, 'end_time': et, 'abstract': abstract,
            'speakers': speakers, 'files': files}

DATA = {
  'conferences': [
    {
      'name': '云原生技术大会', 'acronym': 'CNC 2026', 'year': 2026,
      'location': '上海 · 世博中心', 'start_date': '2026-03-20', 'end_date': '2026-03-21',
      'description': '聚焦 Kubernetes、服务网格、平台工程与云原生 AI 基础设施的年度技术大会，公开全部演讲资料。',
      'source_url': 'https://cnc2026.example.org',
      'sessions': [
        sess('2026-03-20', '云原生', '主题演讲：Kubernetes 的下一个十年', '主厅A', '09:30', '10:15',
             '回顾 Kubernetes 十周年，展望多集群编排、Wasm 集成与 AI 负载调度的演进方向。',
             [sp('张伟', '云启科技', '云启科技首席架构师，CNCF 大使')],
             [fl('主题演讲：Kubernetes 的下一个十年', 'ppt', 'keynote-k8s-next-decade.pptx', 'pptx', 4300, 48, uploaded='2026-03-22'),
              fl('演讲摘要', 'abstract', 'keynote-k8s-abstract.pdf', 'pdf', 210, 2, uploaded='2026-03-18'),
              fl('主题演讲回放', 'video', 'keynote-k8s-replay.mp4', 'mp4', 512000, uploaded='2026-03-25')]),
        sess('2026-03-20', '云原生', '服务网格在生产环境的落地实践', '主厅A', '10:30', '11:15',
             '基于 Istio 的灰度发布、流量治理与零信任安全在大规模集群中的实践经验。',
             [sp('王强', '蓝鲸网络', '蓝鲸网络 SRE 负责人')],
             [fl('服务网格落地实践 演讲稿', 'ppt', 'istio-in-production.pptx', 'pptx', 3600, 39, uploaded='2026-03-22'),
              fl('演讲摘要', 'abstract', 'istio-in-production-abstract.pdf', 'pdf', 180, 2, uploaded='2026-03-18'),
              fl('Istio 配置示例', 'attachment', 'istio-config-samples.zip', 'zip', 96, uploaded='2026-03-22')]),
        sess('2026-03-20', 'DevOps', 'GitOps 流水线设计与多集群发布', '分厅B', '13:00', '13:45',
             '以 ArgoCD 为核心的 GitOps 流水线设计，覆盖 30+ 集群的应用发布与回滚策略。',
             [sp('刘洋', '华云信息', '华云信息资深工程师，Argo 项目贡献者')],
             [fl('GitOps 流水线设计 演讲稿', 'ppt', 'gitops-multicluster.pptx', 'pptx', 2900, 33, uploaded='2026-03-23'),
              fl('演示代码仓库导出', 'attachment', 'gitops-demo-repo.zip', 'zip', 340, uploaded='2026-03-23'),
              fl('演讲回放', 'video', 'gitops-multicluster-replay.mp4', 'mp4', 388000, uploaded='2026-03-26')]),
        sess('2026-03-20', '人工智能', '大模型推理服务的弹性伸缩', '主厅A', '14:00', '14:45',
             '面向 LLM 推理流量的弹性伸缩方案：基于请求队列与 GPU 利用率的混合扩缩容策略。',
             [sp('周婷', '云启科技', '云启科技机器学习工程师'), sp('李娜', '清华大学', '清华大学计算机系副教授')],
             [fl('大模型推理服务的弹性伸缩 演讲稿', 'ppt', 'llm-serving-autoscaling.pptx', 'pptx', 5100, 44, uploaded='2026-03-23'),
              fl('演讲摘要', 'abstract', 'llm-serving-autoscaling-abstract.pdf', 'pdf', 240, 3, uploaded='2026-03-18'),
              fl('压测数据集', 'attachment', 'llm-serving-benchmark.csv', 'csv', 1200, uploaded='2026-03-23')]),
        sess('2026-03-21', '云原生', 'eBPF 可观测性实战', '分厅B', '09:30', '10:15',
             '使用 eBPF 构建零侵入的应用可观测性：网络拓扑、延迟分析与异常检测。',
             [sp('刘洋', '华云信息')],
             [fl('eBPF 可观测性实战 演讲稿', 'ppt', 'ebpf-observability.pptx', 'pptx', 3800, 41, uploaded='2026-03-24'),
              fl('演讲摘要', 'abstract', 'ebpf-observability-abstract.pdf', 'pdf', 190, 2, uploaded='2026-03-19')]),
        sess('2026-03-21', 'DevOps', '平台工程：从理念到落地', '主厅A', '10:30', '11:15',
             '内部开发者平台（IDP）的建设路径：黄金通道、自助服务与平台度量。',
             [sp('郑楠', '华云信息', '华云信息技术 VP')],
             [fl('平台工程：从理念到落地 演讲稿', 'ppt', 'platform-engineering.pptx', 'pptx', 3100, 36, uploaded='2026-03-24',
                 status='blocked', block_reason='含未授权第三方图片，版权投诉处理中'),
              fl('演讲回放', 'video', 'platform-engineering-replay.mp4', 'mp4', 402000, uploaded='2026-03-27')]),
      ],
    },
    {
      'name': '全球AI系统架构峰会', 'acronym': 'AISys 2025', 'year': 2025,
      'location': '北京 · 国家会议中心', 'start_date': '2025-11-14', 'end_date': '2025-11-15',
      'description': '关注大模型训练/推理系统、向量检索与 AI 基础设施架构的国际峰会，议程与论文摘要公开。',
      'source_url': 'https://aisys2025.example.org',
      'sessions': [
        sess('2025-11-14', '人工智能', '万亿参数模型的分布式训练架构', '主厅', '09:30', '10:30',
             '3D 并行、流水线气泡优化与万卡集群的容错训练实践。',
             [sp('李娜', '清华大学'), sp('周婷', '云启科技')],
             [fl('万亿参数模型的分布式训练架构 演讲稿', 'ppt', 'trillion-param-training.pptx', 'pptx', 6800, 56, uploaded='2025-11-17'),
              fl('论文全文', 'paper', 'trillion-param-training-paper.pdf', 'pdf', 2400, 18, lang='英文', uploaded='2025-11-10'),
              fl('演讲回放', 'video', 'trillion-param-training-replay.mp4', 'mp4', 614000, uploaded='2025-11-20')]),
        sess('2025-11-14', '人工智能', '向量数据库与 RAG 系统工程', '分厅1', '11:00', '11:45',
             'RAG 系统的检索质量评估、向量索引选型与混合检索工程化。',
             [sp('陈静', '星图数据', '星图数据数据平台总监')],
             [fl('向量数据库与 RAG 系统工程 演讲稿', 'ppt', 'rag-system-engineering.pptx', 'pptx', 4200, 38, uploaded='2025-11-17'),
              fl('演讲摘要', 'abstract', 'rag-system-engineering-abstract.pdf', 'pdf', 220, 2, uploaded='2025-11-08'),
              fl('RAG 演示代码', 'attachment', 'rag-demo-code.zip', 'zip', 450, uploaded='2025-11-17')]),
        sess('2025-11-14', '数据工程', '实时特征平台建设实践', '分厅2', '14:00', '14:45',
             '支撑在线推理的实时特征平台：特征一致性、点查性能与回灌机制。',
             [sp('吴斌', '星图数据', '星图数据高级工程师')],
             [fl('实时特征平台建设实践 演讲稿', 'ppt', 'realtime-feature-platform.pptx', 'pptx', 3300, 34, uploaded='2025-11-18'),
              fl('演讲摘要', 'abstract', 'realtime-feature-platform-abstract.pdf', 'pdf', 170, 2, uploaded='2025-11-08')]),
        sess('2025-11-15', '人工智能', 'LLM 推理优化：从量化到投机解码', '主厅', '09:30', '10:15',
             'INT4 量化、KV Cache 压缩与投机解码在生产推理中的收益对比。',
             [sp('周婷', '云启科技')],
             [fl('LLM 推理优化 演讲稿', 'ppt', 'llm-inference-optimization.pptx', 'pptx', 4700, 42, uploaded='2025-11-18'),
              fl('演讲回放', 'video', 'llm-inference-optimization-replay.mp4', 'mp4', 489000, uploaded='2025-11-21')]),
        sess('2025-11-15', '数据工程', '湖仓一体架构下的数据治理', '分厅1', '10:30', '11:15',
             '湖仓一体场景下的元数据管理、血缘追踪与数据质量治理体系。',
             [sp('陈静', '星图数据'), sp('吴斌', '星图数据')],
             [fl('湖仓一体架构下的数据治理 演讲稿', 'ppt', 'lakehouse-governance.pptx', 'pptx', 3600, 37, uploaded='2025-11-18'),
              fl('数据治理白皮书', 'paper', 'lakehouse-governance-whitepaper.pdf', 'pdf', 1800, 24, uploaded='2025-11-15')]),
      ],
    },
    {
      'name': '数据工程与分析大会', 'acronym': 'DEA 2025', 'year': 2025,
      'location': '深圳 · 会展中心', 'start_date': '2025-09-05', 'end_date': '2025-09-06',
      'description': '覆盖流批计算、数据质量、日志平台与 BI 分析的数据工程大会，公开 PPT 与回放。',
      'source_url': 'https://dea2025.example.org',
      'sessions': [
        sess('2025-09-05', '数据工程', 'Flink 流批一体的生产实践', '主厅', '09:30', '10:15',
             'Flink 流批一体在实时数仓中的落地：统一 SQL、状态管理与资源弹性。',
             [sp('吴斌', '星图数据')],
             [fl('Flink 流批一体的生产实践 演讲稿', 'ppt', 'flink-stream-batch.pptx', 'pptx', 3900, 40, uploaded='2025-09-08'),
              fl('演讲摘要', 'abstract', 'flink-stream-batch-abstract.pdf', 'pdf', 200, 2, uploaded='2025-09-01'),
              fl('演讲回放', 'video', 'flink-stream-batch-replay.mp4', 'mp4', 433000, uploaded='2025-09-10')]),
        sess('2025-09-05', '数据工程', '数据质量监控体系建设', '分厅A', '11:00', '11:45',
             '从规则引擎到异常检测：覆盖数千张表的数据质量监控体系。',
             [sp('陈静', '星图数据')],
             [fl('数据质量监控体系建设 演讲稿', 'ppt', 'data-quality-monitoring.pptx', 'pptx', 2800, 31, uploaded='2025-09-08'),
              fl('质量规则模板', 'attachment', 'dq-rule-templates.json', 'json', 64, uploaded='2025-09-08')]),
        sess('2025-09-06', '人工智能', '特征平台与模型上线闭环', '主厅', '09:30', '10:15',
             '打通特征平台与模型服务：从特征定义到灰度上线的完整闭环。',
             [sp('周婷', '云启科技')],
             [fl('特征平台与模型上线闭环 演讲稿', 'ppt', 'feature-platform-mlops.pptx', 'pptx', 3200, 35, uploaded='2025-09-09'),
              fl('演讲摘要', 'abstract', 'feature-platform-mlops-abstract.pdf', 'pdf', 190, 2, uploaded='2025-09-02')]),
        sess('2025-09-06', '数据工程', 'PB 级日志平台的成本优化', '分厅A', '10:30', '11:15',
             'PB 级日志平台的存储分层、索引裁剪与查询下推优化，成本下降 60% 的实践。',
             [sp('王强', '蓝鲸网络')],
             [fl('PB 级日志平台的成本优化 演讲稿', 'ppt', 'log-platform-cost-optimization.pptx', 'pptx', 3500, 36, uploaded='2025-09-09'),
              fl('演讲回放', 'video', 'log-platform-cost-replay.mp4', 'mp4', 398000, uploaded='2025-09-12')]),
      ],
    },
    {
      'name': '开源安全峰会', 'acronym': 'OSS 2025', 'year': 2025,
      'location': '线上', 'start_date': '2025-07-11', 'end_date': '2025-07-11',
      'description': '聚焦软件供应链安全、开源合规与漏洞响应的一日线上峰会。',
      'source_url': 'https://oss2025.example.org',
      'sessions': [
        sess('2025-07-11', '安全', '供应链安全：SBOM 落地指南', '直播间1', '10:00', '10:45',
             'SBOM 的生成、交换与消费：在企业内落地软件物料清单的完整指南。',
             [sp('孙磊', '安防实验室', '安防实验室安全研究员')],
             [fl('SBOM 落地指南 演讲稿', 'ppt', 'sbom-in-practice.pptx', 'pptx', 2600, 30, uploaded='2025-07-13'),
              fl('演讲摘要', 'abstract', 'sbom-in-practice-abstract.pdf', 'pdf', 160, 2, uploaded='2025-07-08'),
              fl('SBOM 工具包', 'attachment', 'sbom-toolkit.zip', 'zip', 1800, uploaded='2025-07-13')]),
        sess('2025-07-11', '安全', '开源组件漏洞响应实战', '直播间1', '11:00', '11:45',
             '从漏洞情报到修复闭环：企业级开源组件漏洞响应流程与自动化。',
             [sp('孙磊', '安防实验室'), sp('赵敏', '开源社区', '开源社区布道师')],
             [fl('开源组件漏洞响应实战 演讲稿', 'ppt', 'oss-vuln-response.pptx', 'pptx', 2900, 33, uploaded='2025-07-13'),
              fl('演讲回放', 'video', 'oss-vuln-response-replay.mp4', 'mp4', 356000, uploaded='2025-07-15')]),
        sess('2025-07-11', '开源治理', '企业开源合规体系建设', '直播间2', '14:00', '14:45',
             '许可证合规、CLA 与开源办公室（OSPO）的建设经验。',
             [sp('赵敏', '开源社区')],
             [fl('企业开源合规体系建设 演讲稿', 'ppt', 'oss-compliance.pptx', 'pptx', 2400, 28, uploaded='2025-07-13'),
              fl('演讲摘要', 'abstract', 'oss-compliance-abstract.pdf', 'pdf', 150, 2, uploaded='2025-07-08')]),
        sess('2025-07-11', '安全', '容器镜像扫描的误报治理', '直播间2', '15:00', '15:45',
             '镜像扫描误报的根因分析与治理：可达性分析与 VEX 的应用。',
             [sp('王强', '蓝鲸网络')],
             [fl('容器镜像扫描的误报治理 演讲稿', 'ppt', 'image-scan-false-positive.pptx', 'pptx', 2700, 29, uploaded='2025-07-13')]),
      ],
    },
  ],
  'sample_queries': [
    ['大模型', 18], ['云原生', 15], ['RAG', 12], ['Flink', 9], ['供应链安全', 8],
    ['Kubernetes', 8], ['数据治理', 6], ['SBOM', 5], ['特征平台', 4], ['eBPF', 4],
    ['GitOps', 3], ['向量数据库', 3], ['日志平台', 2], ['平台工程', 2], ['合规', 1],
  ],
}

def main():
    os.makedirs(os.path.join(BASE, 'data'), exist_ok=True)
    path = os.path.join(BASE, 'data', 'import.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(DATA, fh, ensure_ascii=False, indent=2)
    n_sessions = sum(len(c['sessions']) for c in DATA['conferences'])
    n_files = sum(len(s['files']) for c in DATA['conferences'] for s in c['sessions'])
    print('已生成 %s：%d 场会议 / %d 个议程 / %d 个文件' % (path, len(DATA['conferences']), n_sessions, n_files))

if __name__ == '__main__':
    main()
