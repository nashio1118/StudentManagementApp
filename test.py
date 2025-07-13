import React, { useState } from 'react';

import { ChevronLeft, Plus, Edit, Save, X, Calendar, BookOpen, TrendingUp, User } from 'lucide-react';



const StudentManagementApp = () => {

  // サンプル生徒データ

  const [students, setStudents] = useState([

    {

      id: 1,

      name: '田中太郎',

      grade: '中学2年',

      school: '○○中学校',

      notes: '数学が苦手。集中力が続かない傾向。',

      lessons: [

        { date: '2024-07-10', subject: '数学', content: '方程式の解法', homework: '問題集p.20-25', comment: '理解度は良好' },

        { date: '2024-07-08', subject: '英語', content: '現在完了形', homework: '単語テスト準備', comment: '復習が必要' }

      ],

      grades: [

        { subject: '国語', test: '1学期中間テスト', score: 75, maxScore: 100 },

        { subject: '数学', test: '1学期中間テスト', score: 68, maxScore: 100 },

        { subject: '英語', test: '1学期中間テスト', score: 82, maxScore: 100 },

        { subject: '理科', test: '1学期中間テスト', score: 71, maxScore: 100 },

        { subject: '社会', test: '1学期中間テスト', score: 79, maxScore: 100 },

        { subject: '国語', test: '1学期期末テスト', score: 80, maxScore: 100 },

        { subject: '数学', test: '1学期期末テスト', score: 72, maxScore: 100 },

        { subject: '英語', test: '1学期期末テスト', score: 85, maxScore: 100 }

      ]

    },

    {

      id: 2,

      name: '佐藤花子',

      grade: '中学3年',

      school: '△△中学校',

      notes: '受験対策重点。志望校は○○高校。',

      lessons: [

        { date: '2024-07-11', subject: '数学', content: '二次関数', homework: '過去問3年分', comment: '応用問題に挑戦' }

      ],

      grades: [

        { subject: '数学', test: '第1回模試', score: 78, maxScore: 100 },

        { subject: '英語', test: '第1回模試', score: 85, maxScore: 100 }

      ]

    },

    {

      id: 3,

      name: '鈴木一郎',

      grade: '中学1年',

      school: '××中学校',

      notes: '新入生。基礎から丁寧に指導。',

      lessons: [

        { date: '2024-07-09', subject: '数学', content: '正負の数', homework: '基本問題復習', comment: '順調に理解中' }

      ],

      grades: [

        { subject: '数学', test: '小テスト', score: 92, maxScore: 100 }

      ]

    }

  ]);



  const [currentView, setCurrentView] = useState('list');

  const [selectedStudent, setSelectedStudent] = useState(null);

  const [activeTab, setActiveTab] = useState('info');

  const [editMode, setEditMode] = useState(false);

  const [editData, setEditData] = useState({});

  const [showGradeModal, setShowGradeModal] = useState(false);

  const [newGradeData, setNewGradeData] = useState({ grade: '', testName: '' });

  const [expandedTests, setExpandedTests] = useState({});



  const selectStudent = (student) => {

    setSelectedStudent(student);

    setCurrentView('detail');

    setActiveTab('info');

    setEditMode(false);

  };



  const startEdit = () => {

    setEditMode(true);

    setEditData(selectedStudent);

  };



  const saveEdit = () => {

    setStudents(students.map(s => s.id === editData.id ? editData : s));

    setSelectedStudent(editData);

    setEditMode(false);

  };



  const cancelEdit = () => {

    setEditMode(false);

    setEditData({});

  };



  const updateEditData = (field, value) => {

    setEditData(prev => ({

      ...prev,

      [field]: value

    }));

  };



  const addNewLesson = () => {

    const newLesson = {

      date: new Date().toISOString().split('T')[0],

      subject: '',

      content: '',

      homework: '',

      comment: ''

    };

    setEditData(prev => ({

      ...prev,

      lessons: [newLesson, ...(prev.lessons || [])]

    }));

  };



  const addNewGrade = () => {

    setNewGradeData({ grade: '', testName: '' });

    setShowGradeModal(true);

  };



  const createGradeSet = () => {

    if (!newGradeData.grade || !newGradeData.testName) return;

    

    const subjects = ['国語', '数学', '英語', '社会', '理科'];

    const newGrades = subjects.map(subject => ({

      subject,

      test: newGradeData.testName,

      grade: newGradeData.grade,

      score: 0,

      maxScore: 100,

      average: 0

    }));

    

    // 合計点も追加

    newGrades.push({

      subject: '合計点',

      test: newGradeData.testName,

      grade: newGradeData.grade,

      score: 0,

      maxScore: 500,

      average: 0

    });

    

    setEditData(prev => ({

      ...prev,

      grades: [...(prev.grades || []), ...newGrades]

    }));

    

    setShowGradeModal(false);

    setNewGradeData({ grade: '', testName: '' });

  };



  const updateGradeScore = (testName, subject, field, value) => {

    const newGrades = [...editData.grades];

    const gradeIndex = newGrades.findIndex(g => g.test === testName && g.subject === subject);

    

    if (gradeIndex !== -1) {

      newGrades[gradeIndex] = {

        ...newGrades[gradeIndex],

        [field]: parseInt(value) || 0

      };

      

      // 合計点を自動計算

      if (subject !== '合計点') {

        const testGrades = newGrades.filter(g => g.test === testName && g.subject !== '合計点');

        const totalScore = testGrades.reduce((sum, g) => sum + (g.score || 0), 0);

        const totalMaxScore = testGrades.reduce((sum, g) => sum + (g.maxScore || 0), 0);

        

        const totalGradeIndex = newGrades.findIndex(g => g.test === testName && g.subject === '合計点');

        if (totalGradeIndex !== -1) {

          newGrades[totalGradeIndex] = {

            ...newGrades[totalGradeIndex],

            score: totalScore,

            maxScore: totalMaxScore

          };

        }

      }

      

      updateEditData('grades', newGrades);

    }

  };



  const toggleTestExpansion = (testName) => {

    setExpandedTests(prev => ({

      ...prev,

      [testName]: !prev[testName]

    }));

  };



  if (currentView === 'list') {

    return (

      <div className="min-h-screen bg-gray-50 p-4">

        <div className="max-w-md mx-auto">

          <div className="bg-white rounded-lg shadow-sm">

            <div className="p-4 border-b">

              <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">

                <BookOpen className="w-6 h-6 text-blue-600" />

                生徒管理

              </h1>

            </div>

            

            <div className="p-4">

              <div className="space-y-3">

                {students.map(student => (

                  <div

                    key={student.id}

                    onClick={() => selectStudent(student)}

                    className="p-4 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"

                  >

                    <div className="flex items-center gap-3">

                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">

                        <User className="w-5 h-5 text-blue-600" />

                      </div>

                      <div>

                        <h3 className="font-semibold text-gray-800">{student.name}</h3>

                        <p className="text-sm text-gray-600">{student.grade}</p>

                      </div>

                    </div>

                  </div>

                ))}

              </div>

            </div>

          </div>

        </div>

      </div>

    );

  }



  if (currentView === 'detail') {

    const displayData = editMode ? editData : selectedStudent;

    

    return (

      <div className="min-h-screen bg-gray-50">

        {/* ヘッダー */}

        <div className="bg-white shadow-sm p-4">

          <div className="flex items-center justify-between">

            <div className="flex items-center gap-3">

              <ChevronLeft 

                className="w-6 h-6 text-gray-600 cursor-pointer"

                onClick={() => setCurrentView('list')}

              />

              <h1 className="text-lg font-semibold text-gray-800">

                {displayData.name}

              </h1>

            </div>

            <div className="flex gap-2">

              {editMode ? (

                <>

                  <button

                    onClick={saveEdit}

                    className="p-2 text-green-600 hover:bg-green-50 rounded"

                  >

                    <Save className="w-5 h-5" />

                  </button>

                  <button

                    onClick={cancelEdit}

                    className="p-2 text-gray-600 hover:bg-gray-50 rounded"

                  >

                    <X className="w-5 h-5" />

                  </button>

                </>

              ) : (

                <button

                  onClick={startEdit}

                  className="p-2 text-blue-600 hover:bg-blue-50 rounded"

                >

                  <Edit className="w-5 h-5" />

                </button>

              )}

            </div>

          </div>

        </div>



        {/* タブナビゲーション */}

        <div className="bg-white border-b">

          <div className="flex">

            <button

              onClick={() => setActiveTab('info')}

              className={`flex-1 py-3 px-4 text-center border-b-2 ${

                activeTab === 'info' 

                  ? 'border-blue-500 text-blue-600' 

                  : 'border-transparent text-gray-500'

              }`}

            >

              <User className="w-5 h-5 mx-auto mb-1" />

              <span className="text-sm">基本情報</span>

            </button>

            <button

              onClick={() => setActiveTab('lessons')}

              className={`flex-1 py-3 px-4 text-center border-b-2 ${

                activeTab === 'lessons' 

                  ? 'border-blue-500 text-blue-600' 

                  : 'border-transparent text-gray-500'

              }`}

            >

              <Calendar className="w-5 h-5 mx-auto mb-1" />

              <span className="text-sm">授業記録</span>

            </button>

            <button

              onClick={() => setActiveTab('grades')}

              className={`flex-1 py-3 px-4 text-center border-b-2 ${

                activeTab === 'grades' 

                  ? 'border-blue-500 text-blue-600' 

                  : 'border-transparent text-gray-500'

              }`}

            >

              <TrendingUp className="w-5 h-5 mx-auto mb-1" />

              <span className="text-sm">成績</span>

            </button>

          </div>

        </div>



        {/* コンテンツ */}

        <div className="p-4">

          {activeTab === 'info' && (

            <div className="bg-white rounded-lg shadow-sm p-4">

              <div className="space-y-4">

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    名前

                  </label>

                  {editMode ? (

                    <input

                      type="text"

                      value={editData.name}

                      onChange={(e) => updateEditData('name', e.target.value)}

                      className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                    />

                  ) : (

                    <p className="text-gray-800">{displayData.name}</p>

                  )}

                </div>

                

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    学年

                  </label>

                  {editMode ? (

                    <input

                      type="text"

                      value={editData.grade}

                      onChange={(e) => updateEditData('grade', e.target.value)}

                      className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                    />

                  ) : (

                    <p className="text-gray-800">{displayData.grade}</p>

                  )}

                </div>

                

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    学校名

                  </label>

                  {editMode ? (

                    <input

                      type="text"

                      value={editData.school}

                      onChange={(e) => updateEditData('school', e.target.value)}

                      className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                    />

                  ) : (

                    <p className="text-gray-800">{displayData.school}</p>

                  )}

                </div>

                

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    連絡先

                  </label>

                  {editMode ? (

                    <input

                      type="text"

                      value={editData.contact}

                      onChange={(e) => updateEditData('contact', e.target.value)}

                      className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                    />

                  ) : (

                    <p className="text-gray-800">{displayData.contact}</p>

                  )}

                </div>

                

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    留意事項

                  </label>

                  {editMode ? (

                    <textarea

                      value={editData.notes}

                      onChange={(e) => updateEditData('notes', e.target.value)}

                      rows="3"

                      className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                    />

                  ) : (

                    <p className="text-gray-800">{displayData.notes}</p>

                  )}

                </div>

              </div>

            </div>

          )}



          {activeTab === 'lessons' && (

            <div className="space-y-4">

              {editMode && (

                <button

                  onClick={addNewLesson}

                  className="w-full p-3 border-2 border-dashed border-blue-300 rounded-lg text-blue-600 hover:bg-blue-50 flex items-center justify-center gap-2"

                >

                  <Plus className="w-5 h-5" />

                  新しい授業記録を追加

                </button>

              )}

              

              {(displayData.lessons || []).map((lesson, index) => (

                <div key={index} className="bg-white rounded-lg shadow-sm p-4">

                  <div className="space-y-3">

                    <div className="flex gap-2">

                      <div className="flex-1">

                        <label className="block text-sm font-medium text-gray-700 mb-1">

                          日付

                        </label>

                        {editMode ? (

                          <input

                            type="date"

                            value={lesson.date}

                            onChange={(e) => {

                              const newLessons = [...editData.lessons];

                              newLessons[index] = {...lesson, date: e.target.value};

                              updateEditData('lessons', newLessons);

                            }}

                            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                          />

                        ) : (

                          <p className="text-sm text-gray-600">{lesson.date}</p>

                        )}

                      </div>

                      <div className="flex-1">

                        <label className="block text-sm font-medium text-gray-700 mb-1">

                          科目

                        </label>

                        {editMode ? (

                          <input

                            type="text"

                            value={lesson.subject}

                            onChange={(e) => {

                              const newLessons = [...editData.lessons];

                              newLessons[index] = {...lesson, subject: e.target.value};

                              updateEditData('lessons', newLessons);

                            }}

                            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                          />

                        ) : (

                          <p className="text-sm font-semibold text-blue-600">{lesson.subject}</p>

                        )}

                      </div>

                    </div>

                    

                    <div>

                      <label className="block text-sm font-medium text-gray-700 mb-1">

                        内容

                      </label>

                      {editMode ? (

                        <textarea

                          value={lesson.content}

                          onChange={(e) => {

                            const newLessons = [...editData.lessons];

                            newLessons[index] = {...lesson, content: e.target.value};

                            updateEditData('lessons', newLessons);

                          }}

                          rows="3"

                          className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                        />

                      ) : (

                        <p className="text-gray-800 whitespace-pre-line">{lesson.content}</p>

                      )}

                    </div>

                    

                    <div>

                      <label className="block text-sm font-medium text-gray-700 mb-1">

                        宿題

                      </label>

                      {editMode ? (

                        <textarea

                          value={lesson.homework}

                          onChange={(e) => {

                            const newLessons = [...editData.lessons];

                            newLessons[index] = {...lesson, homework: e.target.value};

                            updateEditData('lessons', newLessons);

                          }}

                          rows="3"

                          className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                        />

                      ) : (

                        <p className="text-gray-800 whitespace-pre-line">{lesson.homework}</p>

                      )}

                    </div>

                    

                    <div>

                      <label className="block text-sm font-medium text-gray-700 mb-1">

                        コメント

                      </label>

                      {editMode ? (

                        <textarea

                          value={lesson.comment}

                          onChange={(e) => {

                            const newLessons = [...editData.lessons];

                            newLessons[index] = {...lesson, comment: e.target.value};

                            updateEditData('lessons', newLessons);

                          }}

                          rows="2"

                          className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                        />

                      ) : (

                        <p className="text-gray-800">{lesson.comment}</p>

                      )}

                    </div>

                  </div>

                </div>

              ))}

            </div>

          )}



          {activeTab === 'grades' && (

            <div className="space-y-4">

              {editMode && (

                <button

                  onClick={addNewGrade}

                  className="w-full p-3 border-2 border-dashed border-blue-300 rounded-lg text-blue-600 hover:bg-blue-50 flex items-center justify-center gap-2"

                >

                  <Plus className="w-5 h-5" />

                  新しい成績を追加

                </button>

              )}

              

              {(() => {

                const grades = displayData.grades || [];

                // テスト別にグループ化

                const groupedGrades = grades.reduce((acc, grade) => {

                  const testName = grade.test || 'その他';

                  if (!acc[testName]) {

                    acc[testName] = [];

                  }

                  acc[testName].push(grade);

                  return acc;

                }, {});



                return Object.entries(groupedGrades).map(([testName, testGrades]) => {

                  const isExpanded = expandedTests[testName];

                  const totalGrade = testGrades.find(g => g.subject === '合計点');

                  

                  return (

                    <div key={testName} className="bg-white rounded-lg shadow-sm">

                      <div 

                        className="bg-blue-50 p-3 border-b cursor-pointer hover:bg-blue-100 transition-colors"

                        onClick={() => toggleTestExpansion(testName)}

                      >

                        <div className="flex justify-between items-center">

                          <h3 className="font-semibold text-blue-800">{testName}</h3>

                          <div className="flex items-center gap-2">

                            {totalGrade && (

                              <span className="text-sm text-blue-600">

                                合計: {totalGrade.score}/{totalGrade.maxScore}

                              </span>

                            )}

                            <ChevronLeft 

                              className={`w-4 h-4 text-blue-600 transform transition-transform ${

                                isExpanded ? 'rotate-90' : '-rotate-90'

                              }`}

                            />

                          </div>

                        </div>

                      </div>

                      

                      {isExpanded && (

                        <div className="p-3 space-y-3">

                          {testGrades.map((grade, index) => {

                            const originalIndex = grades.indexOf(grade);

                            return (

                              <div key={originalIndex} className="border rounded-lg p-3">

                                <div className="flex gap-2 mb-3">

                                  <div className="flex-1">

                                    <label className="block text-sm font-medium text-gray-700 mb-1">

                                      科目

                                    </label>

                                    <p className="text-sm font-semibold text-blue-600">{grade.subject}</p>

                                  </div>

                                  <div className="flex-1">

                                    <label className="block text-sm font-medium text-gray-700 mb-1">

                                      学年

                                    </label>

                                    <p className="text-sm text-gray-600">{grade.grade}</p>

                                  </div>

                                </div>

                                

                                <div className="grid grid-cols-3 gap-2">

                                  <div>

                                    <label className="block text-sm font-medium text-gray-700 mb-1">

                                      得点

                                    </label>

                                    {editMode && grade.subject !== '合計点' ? (

                                      <input

                                        type="number"

                                        value={grade.score}

                                        onChange={(e) => updateGradeScore(testName, grade.subject, 'score', e.target.value)}

                                        className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                                      />

                                    ) : (

                                      <p className="text-lg font-bold text-gray-800">{grade.score}</p>

                                    )}

                                  </div>

                                  <div>

                                    <label className="block text-sm font-medium text-gray-700 mb-1">

                                      満点

                                    </label>

                                    {editMode && grade.subject !== '合計点' ? (

                                      <input

                                        type="number"

                                        value={grade.maxScore}

                                        onChange={(e) => updateGradeScore(testName, grade.subject, 'maxScore', e.target.value)}

                                        className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                                      />

                                    ) : (

                                      <p className="text-lg text-gray-600">{grade.maxScore}</p>

                                    )}

                                  </div>

                                  <div>

                                    <label className="block text-sm font-medium text-gray-700 mb-1">

                                      平均点

                                    </label>

                                    {editMode && grade.subject !== '合計点' ? (

                                      <input

                                        type="number"

                                        value={grade.average}

                                        onChange={(e) => updateGradeScore(testName, grade.subject, 'average', e.target.value)}

                                        className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                                      />

                                    ) : (

                                      <p className="text-lg text-gray-600">{grade.average}</p>

                                    )}

                                  </div>

                                </div>

                              </div>

                            );

                          })}

                        </div>

                      )}

                    </div>

                  );

                });

              })()}

            </div>

          )}

        </div>

        

        {/* 成績追加モーダル */}

        {showGradeModal && (

          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">

            <div className="bg-white rounded-lg p-6 w-80 max-w-sm mx-4">

              <h3 className="text-lg font-semibold text-gray-800 mb-4">

                学年・テスト名を入力してください

              </h3>

              

              <div className="space-y-4">

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    学年

                  </label>

                  <select

                    value={newGradeData.grade}

                    onChange={(e) => setNewGradeData(prev => ({...prev, grade: e.target.value}))}

                    className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                  >

                    <option value="">選択してください</option>

                    <option value="中1">中1</option>

                    <option value="中2">中2</option>

                    <option value="中3">中3</option>

                    <option value="高1">高1</option>

                    <option value="高2">高2</option>

                    <option value="高3">高3</option>

                  </select>

                </div>

                

                <div>

                  <label className="block text-sm font-medium text-gray-700 mb-1">

                    テスト名

                  </label>

                  <input

                    type="text"

                    value={newGradeData.testName}

                    onChange={(e) => setNewGradeData(prev => ({...prev, testName: e.target.value}))}

                    placeholder="例: 1学期期末テスト"

                    className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"

                  />

                </div>

              </div>

              

              <div className="flex gap-2 mt-6">

                <button

                  onClick={() => setShowGradeModal(false)}

                  className="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"

                >

                  キャンセル

                </button>

                <button

                  onClick={createGradeSet}

                  disabled={!newGradeData.grade || !newGradeData.testName}

                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"

                >

                  作成

                </button>

              </div>

            </div>

          </div>

        )}

      </div>

    );

  }

};



export default StudentManagementApp;
