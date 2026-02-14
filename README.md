# GraphQL Tutorial - Complete Project Index

This is a comprehensive learning guide for **GraphQL with Django and Graphene**, structured across 5 progressive apps.

## 📚 Learning Path Overview

```
App 1: Basics           → App 2: CRUD & Relations    → App 3: Filtering & Pagination
       ↓                        ↓                              ↓
    [Query]              [Mutations & Validation]        [Advanced Queries]
    [Models]             [Relationships]                 [Aliases & Fragments]
```

```
App 4: Auth & Permissions    → App 5: Performance & Production
       ↓                              ↓
   [Secure API]                  [Optimization]
   [Role-Based Access]           [Testing]
                                 [Deployment]
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

### **App 2: Mutations, Validation & Relationships** 🔄 Ready to build
Location: `app2_mutations/` (to be created)

**Topics to cover:**
- Create mutations (POST operations)
- Update mutations
- Delete mutations
- Input type validation
- Error handling
- ForeignKey relationships
- OneToOne relationships
- ManyToMany relationships
- Nested queries

**Dependencies:** Requires understanding of App 1

---

### **App 3: Filtering, Sorting, Pagination & Advanced Queries** 🔄 Ready to build
Location: `app3_filtering/` (to be created)

**Topics to cover:**
- Filtering with django-filter
- Multiple filter conditions
- Sorting/ordering
- Offset-based pagination
- Cursor-based pagination
- Relay pagination
- Query aliases
- Fragments
- Variables in queries

**Dependencies:** Requires understanding of App 1 & 2

---

### **App 4: Authentication, Authorization & Permissions** 🔄 Ready to build
Location: `app4_authentication/` (to be created)

**Topics to cover:**
- User authentication
- Token-based auth
- JWT tokens
- Login/logout mutations
- Permission checking
- Role-based access control
- Field-level permissions
- Middleware for auth

**Dependencies:** Requires understanding of App 1-3

---

### **App 5: Performance, Testing, Real-time & Production** 🔄 Ready to build
Location: `app5_production/` (to be created)

**Topics to cover:**
- N+1 query problem & solutions
- DataLoader implementation
- Caching strategies
- Query complexity analysis
- Rate limiting
- WebSocket subscriptions
- Unit testing resolvers
- Integration testing
- Logging & monitoring
- Docker deployment
- Security hardening

**Dependencies:** Requires understanding of all previous apps

---

## 🚀 Getting Started

### Quick Start - App 1 Only
```bash
cd app1_basics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < add_sample_data.py
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/graphql/`

### Full Project Setup (All Apps)
```bash
# Each app has its own virtual environment and database
# Follow the QUICKSTART.md in each app directory
```

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
- [ ] Learn App 5: Production-ready code
- [ ] Implement complete real-world project
- [ ] Deploy using Docker

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

### App 5: Production
- **Performance** - Query optimization
- **Testing** - Comprehensive test coverage
- **Real-time** - WebSocket subscriptions
- **Deployment** - Container & cloud ready

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
graphql_tutorial/
├── .github/
│   └── instructions/
│       └── 5-apps-learning-path.md
├── app1_basics/                    ✅ Complete
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── schema.py
│   ├── basics_app/
│   │   ├── models.py
│   │   └── migrations/
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── add_sample_data.py
│   └── tests.py
├── app2_mutations/                 🔄 To be created
├── app3_filtering/                 🔄 To be created
├── app4_authentication/            🔄 To be created
├── app5_production/                🔄 To be created
└── INDEX.md                        (this file)
```

---

## ✅ Checklist

### App 1 (Completed)
- [x] Project setup
- [x] Django configuration
- [x] Models (Author, Book)
- [x] GraphQL schema
- [x] Query resolvers
- [x] Sample data script
- [x] Documentation
- [x] Quick start guide
- [x] Tests

### App 2 (Next)
- [ ] Mutation classes
- [ ] Input types
- [ ] Create operation
- [ ] Update operation
- [ ] Delete operation
- [ ] Error handling
- [ ] Relationship examples

---

## 🤔 FAQs

**Q: Can I skip Apps?**
A: No, each app builds on the previous. Follow the order: 1 → 2 → 3 → 4 → 5

**Q: How long does each app take?**
A: App 1: 2-3 hrs, App 2: 3-4 hrs, App 3: 3-4 hrs, App 4: 4-5 hrs, App 5: 6-8 hrs

**Q: Do I need Django experience?**
A: Helpful but not required. App 1 teaches the basics.

**Q: Can I use this in production?**
A: App 5 is production-ready. Earlier apps are for learning.

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
✅ Optimize and deploy production applications  
✅ Test GraphQL APIs comprehensively  
✅ Implement real-time features with subscriptions  

---

## 🤝 Contributing

These tutorials are open source. Feel free to suggest improvements or corrections!

---

## 📝 Progress Tracking

Track your progress through the apps:

- **App 1:** ████████████████████ 100% ✅
- **App 2:** ░░░░░░░░░░░░░░░░░░░░  0% (Start next)
- **App 3:** ░░░░░░░░░░░░░░░░░░░░  0%
- **App 4:** ░░░░░░░░░░░░░░░░░░░░  0%
- **App 5:** ░░░░░░░░░░░░░░░░░░░░  0%

**Overall: 20% Complete**

---

## 🎉 Ready to Start?

Begin with App 1:
```bash
cd app1_basics
cat QUICKSTART.md
```

**Happy Learning!** 🚀

