# GraphQL Tutorial - Complete Learning Repository

A comprehensive **open-source learning guide** for **GraphQL with Django and Graphene**, structured across 5 progressive apps. This repository is designed for developers to learn and follow along with hands-on examples and best practices.

## 📚 Learning Path Overview

```
App 1: Basics           → App 2: CRUD & Relations    → App 3: Filtering & Pagination
       ↓                        ↓                              ↓
    [Query]              [Mutations & Validation]        [Advanced Queries]
    [Models]             [Relationships]                 [Aliases & Fragments]
```

```
App 4: Auth & Permissions    → App 5: Performance & Real-time
       ↓                              ↓
   [Secure API]                  [Query Optimization]
   [Role-Based Access]           [Caching Strategies]
                                 [Real-time Updates]
```

---

## 🎯 Apps Overview

### **App 1: GraphQL Basics & Django Models** ✅ Complete
Location: `app1_basics/`

**What you'll learn:**
- GraphQL fundamentals
- Setting up Graphene with Django
- Converting Django models to GraphQL types
- Writing basic queries
- Fetching single and multiple records
- Testing with GraphiQL

**Duration:** ~2-3 hours  
**Status:** Ready to use

**Key Files:**
- [README.md](app1_basics/README.md) - Full documentation
- [QUICKSTART.md](app1_basics/QUICKSTART.md) - 5-minute setup
- [schema.py](app1_basics/config/schema.py) - Schema definition
- [models.py](app1_basics/basics_app/models.py) - Data models

---

### **App 2: Mutations, Validation & Relationships** ✅ Complete
Location: `app2_mutations/`

**What you'll learn:**
- Write operations (Create, Update, Delete)
- Mutations with input validation
- Error handling strategies
- ForeignKey, OneToOne, and ManyToMany relationships
- Nested query patterns
- Input type design

**Duration:** ~3-4 hours  
**Status:** Ready to use

**Key Files:**
- [README.md](app2_mutations/README.md) - Complete documentation
- [QUICKSTART.md](app2_mutations/QUICKSTART.md) - Quick setup guide
- [schema.py](app2_mutations/config/schema.py) - Mutations & schema

---

### **App 3: Filtering, Sorting, Pagination & Advanced Queries** ✅ Complete
Location: `app3_filtering/`

**What you'll learn:**
- Advanced filtering with django-filter
- Sorting and ordering strategies
- Offset-based pagination (page/limit)
- Cursor-based pagination (Relay-style)
- Query variables and reusable patterns
- Aliases and fragments
- Complex multi-filter queries

**Duration:** ~3-4 hours  
**Status:** Ready to use

**Key Files:**
- [README.md](app3_filtering/README.md) - Full documentation
- [QUICKSTART.md](app3_filtering/QUICKSTART.md) - Quick setup guide
- [schema.py](app3_filtering/config/schema.py) - Filtering & pagination

---

### **App 4: Authentication, Authorization & Permissions** ✅ Complete
Location: `app4_auth/`

**What you'll learn:**
- User registration and authentication
- JWT token generation and validation
- Login/logout mutations
- Permission decorators
- Role-based access control (RBAC)
- Activity logging and audit trails
- Secure mutation patterns

**Duration:** ~4-5 hours  
**Status:** Ready to use

**Key Files:**
- [README.md](app4_auth/README.md) - Complete documentation
- [QUICKSTART.md](app4_auth/QUICKSTART.md) - Quick setup guide
- [schema.py](app4_auth/config/schema.py) - Auth & permissions

---

### **App 5: Performance Optimization & Real-time** ✅ Complete
Location: `app5_performance/`

**What you'll learn:**
- N+1 query problem and solutions (select_related, prefetch_related)
- Database indexing strategies
- Caching patterns with Redis
- Query optimization techniques
- Performance monitoring
- Real-time capabilities with GraphQL subscriptions

**Duration:** ~6-8 hours  
**Status:** Ready to use

**Key Files:**
- [README.md](app5_performance/README.md) - Complete documentation
- [QUICKSTART.md](app5_performance/QUICKSTART.md) - Quick setup guide
- [schema.py](app5_performance/config/schema.py) - Optimized resolvers

---

---

## 🚀 Getting Started

### Clone the Repository
```bash
git clone https://github.com/yourusername/graphql_tutorial.git
cd graphql_tutorial
```

### Quick Start - App 1 Only
```bash
cd app1_basics
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python add_sample_data.py
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/graphql/`

### Full Project Setup (All Apps)
Each app is **completely independent** with its own:
- Virtual environment
- Database (SQLite)
- Dependencies
- Sample data

Follow the `QUICKSTART.md` in each app directory to get up and running in minutes.

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| [5-apps-learning-path.md](.github/instructions/5-apps-learning-path.md) | Learning structure & topics |
| [app1_basics/README.md](app1_basics/README.md) | Complete App 1 documentation |
| [app1_basics/QUICKSTART.md](app1_basics/QUICKSTART.md) | 5-minute setup guide |

---

## 🎓 Learning Recommendations

### Beginner (Week 1)
- [ ] Read App 1 README.md
- [ ] Complete App 1 QUICKSTART.md
- [ ] Test all example queries in GraphiQL
- [ ] Modify queries to explore different fields
- [ ] Review the schema.py file extensively

### Intermediate (Week 2)
- [ ] Start App 2: Learn mutations
- [ ] Understand input validation
- [ ] Practice creating, updating, deleting
- [ ] Start App 3: Learn filtering and pagination

### Advanced (Week 3+)
- [ ] Complete App 4: Authentication & security
- [ ] Learn App 5: Performance optimization
- [ ] Implement complete real-world project
- [ ] Understand optimization patterns

---

## 💡 Key Concepts by App

### App 1: Fundamentals
- **ObjectType** - Maps Django model to GraphQL
- **Query** - Read operations
- **Resolver** - Function that fetches data
- **Schema** - Complete API definition

### App 2: Write Operations
- **Mutation** - Create/update/delete operations
- **Input Types** - Validated input structures
- **Validation** - Field and business logic validation
- **Relationships** - FK, O2O, M2M in GraphQL

### App 3: Query Optimization
- **Filtering** - Dynamic query parameters
- **Pagination** - Handle large datasets
- **Variables** - Reusable query templates
- **Fragments** - Code reuse in queries

### App 4: Security
- **Authentication** - Identify users
- **Authorization** - Control access
- **Middleware** - Request interceptors
- **Permissions** - Field & operation level

### App 5: Performance
- **Optimization** - Query optimization
- **Caching** - Optimization strategies
- **Real-time** - WebSocket subscriptions
- **Monitoring** - Performance tracking

---

## 🛠 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Virtual environment** (venv)
- **Basic Django knowledge** (helpful but not required)
- **Text editor or IDE** (VS Code recommended)

---

## 📋 Project Structure

```
├── app1_basics/                    ✅ Complete
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── schema.py
│   │   └── __init__.py
│   ├── basics_app/
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── migrations/
│   │   └── __init__.py
│   ├── graphql/                    (Pure GraphQL operations)
│   │   ├── queries/
│   │   └── fragments/
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── add_sample_data.py
│   └── tests.py
├── app2_mutations/                 ✅ Complete
│   ├── config/
│   ├── mutations_app/
│   ├── graphql/
│   │   ├── queries/
│   │   ├── mutations/
│   │   └── fragments/
│   ├── README.md
│   ├── QUICKSTART.md
│   └── postman/
├── app3_filtering/                 ✅ Complete
│   ├── config/
│   ├── filtering_app/
│   ├── graphql/
│   ├── README.md
│   ├── QUICKSTART.md
│   └── postman/
├── app4_auth/                      ✅ Complete
│   ├── config/
│   ├── auth_app/
│   ├── graphql/
│   ├── README.md
│   ├── QUICKSTART.md
│   └── postman/
├── app5_performance/               ✅ Complete
│   ├── config/
│   ├── perf_app/
│   ├── graphql/
│   ├── README.md
│   ├── QUICKSTART.md
│   └── postman/
├── .gitignore                      (Version control exclusions)
└── README.md                       (This file)
```

---

## ✅ What's Included

### Each App Contains:
- ✅ **Complete Django + Graphene setup** - Ready to run
- ✅ **Well-documented code** - Learn by reading
- ✅ **Sample data scripts** - Realistic test data included
- ✅ **Comprehensive README** - Deep explanations & patterns
- ✅ **QUICKSTART guide** - Get running in 5 minutes
- ✅ **Postman collection** - Test all queries with ready-made requests
- ✅ **.graphql files** - Pure GraphQL operations for reference

### Learning Features:
- 📚 **Progressive complexity** - Each app builds on previous
- 🎯 **Real-world patterns** - Industry-standard approaches
- 🔍 **Clear explanations** - Understand every concept
- 💻 **Hands-on practice** - Code along with tutorials
- ⚡ **Performance focused** - Learn optimization techniques

---

## ✅ All 5 Apps Completed

### App 1: GraphQL Basics
- [x] Models mapping to GraphQL types
- [x] Basic queries
- [x] Schema documentation

### App 2: Mutations & CRUD
- [x] Create mutations
- [x] Update and delete operations
- [x] Input validation
- [x] Error handling
- [x] All relationship types (FK, O2O, M2M)

### App 3: Advanced Queries
- [x] django-filter integration
- [x] Complex filtering combinations
- [x] Offset & cursor pagination
- [x] Query variables and reusable fragments
- [x] Sorting and ordering

### App 4: Authentication & Security
- [x] User registration & login
- [x] JWT token generation
- [x] Role-based access control
- [x] Permission decorators
- [x] Secure mutation patterns

### App 5: Performance Optimization
- [x] N+1 query problem & solutions
- [x] Database optimization with indexes
- [x] Caching strategies
- [x] Performance monitoring
- [x] Query optimization patterns

---

## 🤔 FAQs

**Q: Can I skip Apps?**
A: No, each app builds on the previous. Follow the order: 1 → 2 → 3 → 4 → 5

**Q: How long does each app take?**
A: App 1: 2-3 hrs, App 2: 3-4 hrs, App 3: 3-4 hrs, App 4: 4-5 hrs, App 5: 6-8 hrs

**Q: Do I need Django experience?**
A: Helpful but not required. App 1 teaches the basics.

**Q: What about advanced topics?**
A: App 5 covers performance optimization, real-time capabilities, and industry best practices.

---

## 📚 Additional Resources

- [GraphQL Official Docs](https://graphql.org/learn/)
- [Graphene Documentation](https://docs.graphene-python.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

---

## 🎯 Learning Outcomes

After completing all 5 apps, you will be able to:

✅ Design GraphQL APIs from scratch  
✅ Build secure, scalable GraphQL applications  
✅ Implement complex queries and mutations  
✅ Handle authentication and permissions  
✅ Optimize and scale GraphQL applications  
✅ Test GraphQL APIs comprehensively  
✅ Implement real-time features with subscriptions  

---

## 🤝 Contributing

We welcome contributions to this learning repository! Whether it's:
- Bug fixes in the code
- Improvements to documentation
- Additional examples or exercises
- Translation to other languages
- New features or concepts to cover

Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

---

## 📝 Progress Tracking

Track your learning progress through all 5 apps:

- **App 1:** ████████████████████ 100% ✅ Complete
- **App 2:** ████████████████████ 100% ✅ Complete
- **App 3:** ████████████████████ 100% ✅ Complete
- **App 4:** ████████████████████ 100% ✅ Complete
- **App 5:** ████████████████████ 100% ✅ Complete

**Overall: 100% Complete** - All 5 apps ready to learn and follow along! 🎉

---

## 🎉 Ready to Start Learning?

### Start with App 1:
```bash
git clone https://github.com/yourusername/graphql_tutorial.git
cd graphql_tutorial/app1_basics
cat QUICKSTART.md
```

### Or jump to any app:
Each app is **completely independent** - start anywhere that interests you!

- **New to GraphQL?** → Start with [App 1](app1_basics/)
- **Want to build APIs?** → Check out [App 2](app2_mutations/)
- **Need filtering?** → Go to [App 3](app3_filtering/)
- **Need security?** → Study [App 4](app4_auth/)
- **Building scalable apps?** → Learn [App 5](app5_performance/)

---

## ⭐ Star This Repository

If you find this learning resource helpful, please consider **starring** the repository! It helps other developers discover this comprehensive GraphQL learning guide.

## 💬 Questions & Support

For questions or feedback:
- **GitHub Issues** - For bugs or detailed questions
- **Discussions** - For general questions and ideas
- **Pull Requests** - To contribute improvements

---

**Happy Learning! 🚀**

*Learning GraphQL from basics to advanced patterns, one app at a time.*

